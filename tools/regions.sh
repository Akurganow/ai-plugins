# Region helpers, sourced and never run. tools/regenerate.sh and the coming
# tools/build.sh source this file, so the marker rules live only here.
#
# A region inside a hand-written file sits between two lines,
# `<!-- NAME:start -->` and `<!-- NAME:end -->`.
#
#   replace_region FILE NAME CONTENT  fill the region from the lines of CONTENT
#   short_form FILE                   print the text inside the hook-text region
#   full_text FILE                    print FILE without the hook-text region
#   strip_front_matter FILE           print FILE without its front matter
#   write_if_changed SOURCE DEST      copy SOURCE over DEST unless they are equal
#
# replace_region skips a file with neither marker, so a region takes effect
# once someone adds its markers. short_form and full_text fail on such a file,
# because their callers need the region. Every operation stops on any other
# mismatch: a lone marker, a duplicate, the end before the start, or a marker
# line that ends in CR.
#
# The caller defines `die`, which must exit. replace_region also needs `WORK`,
# a writable directory.

# write_if_changed SOURCE DEST: copy SOURCE over DEST unless they are equal,
# creating DEST's directory first. `cat >` keeps DEST's mode; a symlink at
# DEST is removed first, so the copy lands at DEST and not at the link's target.
write_if_changed() {
  mkdir -p "$(dirname "$2")" || die "cannot create the directory of $2"
  if [ -L "$2" ]; then
    rm "$2"
  elif cmp -s "$1" "$2"; then
    return 0
  fi
  cat "$1" >"$2" || die "cannot write $2; check it and its directory are writable"
}

# check_markers FILE REGION RERUN NEED: stops unless FILE holds one start and
# one end line of REGION. NEED is `optional` or `required`; an optional region
# with neither marker makes this return 1 and stop nothing. RERUN names the
# command the error message tells the person to run again.
check_markers() {
  local file=$1 region=$2 rerun=$3 need=$4
  local start="<!-- ${region}:start -->" end="<!-- ${region}:end -->"
  local starts ends
  # A marker line ending in CR matches neither exact pattern below, so the
  # region would be skipped without a word.
  if grep -qxF -e "$start"$'\r' -e "$end"$'\r' -- "$file"; then
    die "$file: region '$region' has CRLF marker lines; convert the file to LF and re-run $rerun"
  fi
  # grep -c exits 1 when it counts zero; only a higher status is an error.
  starts=$(grep -cxF -- "$start" "$file") || [ "$?" -eq 1 ] || die "grep cannot read $file"
  ends=$(grep -cxF -- "$end" "$file") || [ "$?" -eq 1 ] || die "grep cannot read $file"
  [ "$need" = optional ] && [ "$starts" -eq 0 ] && [ "$ends" -eq 0 ] && return 1
  [ "$starts" -eq 1 ] && [ "$ends" -eq 1 ] ||
    die "$file: region '$region' needs one '$start' line and one '$end' line; found $starts and $ends; fix the markers and re-run $rerun"
  return 0
}

# replace_region FILE REGION CONTENT: put the lines of CONTENT between the
# REGION markers in FILE. Blank lines at both ends of CONTENT are dropped.
# One blank line follows the start marker and one precedes the end marker.
replace_region() {
  local file=$1 region=$2 content=$3
  local start="<!-- ${region}:start -->" end="<!-- ${region}:end -->"
  local status=0 out="$WORK/region"
  [ -f "$file" ] || return 0
  check_markers "$file" "$region" "bash tools/regenerate.sh" optional || return 0
  awk -v start="$start" -v end="$end" -v content="$content" '
    $0 == start {
      print
      n = 0
      while ((getline line < content) > 0) body[++n] = line
      close(content)
      first = 1
      while (first <= n && body[first] ~ /^[ \t]*$/) first++
      last = n
      while (last >= first && body[last] ~ /^[ \t]*$/) last--
      print ""
      for (i = first; i <= last; i++) print body[i]
      if (last >= first) print ""
      inside = 1
      next
    }
    $0 == end {
      if (!inside) exit 3
      inside = 0
    }
    !inside { print }
  ' "$file" >"$out" || status=$?
  case $status in
    0) ;;
    3) die "$file: '$end' comes before '$start'; swap the two lines and re-run bash tools/regenerate.sh" ;;
    *) die "$file: awk failed with status $status while filling region '$region'; its error is above" ;;
  esac
  write_if_changed "$out" "$file"
}

# region_bounds FILE REGION: sets region_first and region_last to the line
# numbers of the start and end markers. Both exist exactly once, as
# check_markers requires, so the two numbers are single values.
region_bounds() {
  local file=$1 region=$2
  local start="<!-- ${region}:start -->" end="<!-- ${region}:end -->"
  check_markers "$file" "$region" "bash tools/build.sh" required
  region_first=$(grep -nxF -- "$start" "$file" | cut -d: -f1)
  region_last=$(grep -nxF -- "$end" "$file" | cut -d: -f1)
  [ "$region_first" -lt "$region_last" ] ||
    die "$file: '$end' comes before '$start'; swap the two lines and re-run bash tools/build.sh"
}

# short_form FILE: the text between the hook-text markers, without the blank
# line replace_region puts after the start marker and before the end marker.
# A line in those places that is not blank is text, so it stays.
short_form() {
  region_bounds "$1" hook-text
  awk -v s="$region_first" -v e="$region_last" '
    NR > s && NR < e && !((NR == s + 1 || NR == e - 1) && /^[ \t]*$/)
  ' "$1"
}

# full_text FILE: FILE without the hook-text region, markers included, so no
# copy of the full text can carry the short form.
full_text() {
  region_bounds "$1" hook-text
  awk -v s="$region_first" -v e="$region_last" 'NR < s || NR > e' "$1"
}

# strip_front_matter FILE: FILE without a leading `---` ... `---` block.
strip_front_matter() {
  awk '
    NR == 1 && /^---[ \t]*$/ { in_front = 1; next }
    in_front && /^---[ \t]*$/ { in_front = 0; next }
    !in_front { print }
  ' "$1"
}
