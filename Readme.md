
# Static Html Pre-processor

Compiles HTML from files with easy to read SHP syntax.

#### User defined language
To enable SHP syntax coloring in Notepad++ import `npp_udl_shp.xml` in `Language > User Defined Language > Define your language... > Import`. Then choose `shp` from the languages list.

# SHP Syntax

```shp
@doctype[#HTML]
$html {
  $head {
    %meta[charset 'utf-8']
    %link[rel stylesheet href '/stylesheets/index.css']
  }
  $body {
    $div[#Content .bigText] {
      Hello world!
    }
  }
}
```

## Tags and scopes

In `SHP` there are two tag types - `scoped` and `scopeless`. 

#### `Scoped` tags

Scoped tags are prefixed with `$` and are compiled to have both beginning and finishing tokens. For example `<div></div>`. Scoped tags can have content (text or other tags) inside of them. Add curly brackets to put content inside of a tag `$div { Inside }`. Omitting brackets of a `scoped` tag also produces valid code (`$div $div` creates two tags that are next to each other)

#### `Scopeless` tags

Scopeless tags are prefixed with `%` and are compiled to have only beginning token. For example `<img>` or `<link>`. This type of tag can't have any content inside.

#### Summary

- `$div` - Scoped but no content, produces `<div></div>`
- `$div { Content }` - Scoped with content, produces `<div> Content </div> `
- `%meta` - Scopeless, produces `<meta>`

The tag type is not detected from the tag name. This means you have to choose it yourself.

## Parameters

Tags parameters can be added within square brackets `[]`. These brackets must be added right after the tag name.

Generally, parameters can be added to the element by typing its name and then value. In contrary to HTML, equal sign is not used, like so `$div[width 300 height 200]`.

Some parameters can be added using prefixes:

- To add element ID type it with a `#` prefix - `$div[#FirstElement]`
- To add a class, add `.` prefix - `$div[.Wide .Dark]`
- To set a bool flag to true, add `!` prefix - `$div[!hidden]`, `$video[!controls]`

Prefixed parameters can be mixed freely with name + value ones. The order does not matter.

#### String enclosing

Parameter values that contain special characters should be enclosed in single ticks `'`

For example `%link[rel stylesheet href 'https://some_cdn.com/file/stylesheet.css']`

#### Relation with content

Parameters should be defined before tag content

```shp
$div[#SecondElement .Wide] {
  Hello world
}
```

#### Summary

- `%link[rel stylesheet]` produces `<link rel=stylesheet>`

- `$div[width 300]` produces `<div width=300></div>`
- `$div[#ThirdElement width 300]` produces `<div id=ThirdElement width=300></div>`
- `$div[width 300 .Wide .Dark]` produces `<div width=300 class="Wide Dark"></div>`
- `$div[width 300 !hidden]` produces `<div width=300 hidden=true></div>`

## Functions

**Note: functions are not available in the Javascript port**

To call a function, prefix its name with a `@`. Parameters can be added like it's normal HTML tag. Some functions can also have associated scope, or a body.

```shp
@functionName[paramName paramValue] {
  $div { Function body }
}
```

#### `define[id] { body }`

Creates a definition with ID `id`. 

#### `doctype[id]`

Adds a doctype clause. `id` parameter defines the doctype. `HTML` is the default value of `id` so in most cases you can omit it completely.

For example `@doctype[#OtherDoctype]` produces `<!DOCTYPE OtherDoctype>`

#### `include[file as]`

Include definitions from SHP file with path `file` and stores them in namespace called `as`. File extension is added automatically.

For example `@include[file './bar' as foo]` includes definitions from `./bar.shp `and saves them in `foo` namespace.

#### `paste[id from]`

Copies body of a definition with ID `id` to where the function is called. Parameter `from` selects which namespace to use (by default it's empty).

#### Define / paste examples

File `bar.shp`

```shp
@define[#header] {
  $header {
    $h1 { Hello world! }
    $p { This header was defined in bar.shp }
  }
}
```

File `index.shp` (entry point)

```shp
@include[file './bar' as bar]

@doctype[#HTML]
$html {
  $head {
    %meta[charset 'utf-8']
    $title { SHP Example }
  }
  $body {
    @paste[#header from bar]
    $div[#content] {
      The rest of the content was defined in index.shp
    }
  }
}
```

Compiling `index.shp` produces the following result
