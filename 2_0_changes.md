# Planned SHP 2.0 changes
These changes are breaking compatibality with SHP 1

## General
- All functional characters can be escaped with a `\`
- Automatic detection whether a tag is scoped. Tags are prefixed with a `$`.
  ```shp
  $body {
    $img[src="path/to/img.png"] // not scoped
    $script[src="path/to/script.js"] // scoped
  }
  ```
- Standard preformatted tags are detected automatically. To explicitly enable preformatted feature use a `%` prefix. Content of preformatted tags (both auto-detected and explicit) is not parsed as SHP.
  ```shp
  $pre {
    $some[shp=code] {that is ignored\}
    until unescaped close bracked is encountered
  }
  %style { // explicit preform.
    html {margin: 0}
  }
  ```
- Add an option to add a space after otherwise not preformatted tags with a `_` suffix. By default the tags are not separated by spaces.
  ```shp
  $b_ {Hello} world // <b>hello</b> world
  $b {Ban} ana // <b>Ban</b>ana
  ```

## Tag attributes
- Restore equal sign `=` in attributes with out quick prefix
  ```shp
  $img[#BannerLogo src="path/to/img.png"]
  ```
- Literals are now exclusively created with `"` double quotes
- Quick flags can be set as true or false with `+` and `!` prefixes respectively
  ```shp
  $div[+hidden] // hidden = true
  $video[!controls] // controls = false
  ```

## Functions
- Functions now accept variables for easier formatting, example
  ```shp
  @define[#MySection ?sectionID] {
    $section[#@[sectionID]]
  }
  ```
- New pair of functions was added: `@slot` / `@insert`, define a slot once and insert into it many times, example
  ```
  $head {@slot[#head]}
  @insert[#head] {$meta[charset='utf-8']}
  @insert[#head] {$title {My webpage}}
  ```
