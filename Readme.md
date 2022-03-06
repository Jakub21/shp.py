# SHP.py

Static HTML Preprocessor

Compiles HTML from files with easy to read SHP syntax.

You might also want to lake a look at the [Javascript port](https://github.com/Jakub21/shp.js) of this project.

#### Notepad++ SHP syntax coloring
You can enable syntax coloring for SHP in the following way

- In the top bar, open `Language` tab
- Navigate to `User Defined Language`, then `Define your language...`
- Choose `Import` and select `./npp_udl_shp.xml` from this repository
- Go back to `Language` tab and select `shp` from the list.

# Installation

To install the package, download it from PIP

```
pip install shp
```

# CLI usage

There is `shp.compile` executable module available

Run the following in your terminal

```
python -m shp.compile <source> <target> <--watch>
```

Arguments:

- `source` (required) - Path to the SHP source file (entry point)
- `target` (required) - Path to the target HTML file
- `-w --watch` - Recompile whenever entry point file or any other included file is edited

# Using SHP as a package

Using `SHP` class to compile from a single entry-point

```python
from shp import SHP
# create an instance
shp = SHP(sourcePath, targetPath)
# compile once
shp.compile()
# compile once, set up a watchdog and block further execution
shp.watch()
```

Using `MultiSHP` class to compile from multiple entry-points

```python
from shp import MultiSHP
# create an instance
mp = MultiSHP()
# add sources and their corresponding targets
mp.add(firstSource, firstTarget)
mp.add(secondSource, secondTarget)
# compile all sources
mp.compile()
# compile all sources, set up their watchdogs and blocks further execution
mp.watch()
```

#### Watching with out blocking

Method responsible for watching can have their blocking disabled by passing `noBlock=False` argument. This works for both `SHP` and `MultiSHP` classes. Make sure the script does not exit.

```python
shp.watch(False)
mp.watch(False)
```

You should stop the watchers before your program ends.

```python
shp.stop()
mp.stop()
```

# SHP Syntax

General example

```shp
// This is a general SHP Syntax example
@doctype
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

Copies the content of selected file in its own place. Namespaces from included files are preserved.

To wrap the copied content in a namespace, use the optional `as` parameter. This defines the ID.

Note that `./` prefix and file extension are excluded.


#### `namespace[id] { body }`

Creates a namespace with ID `id`. Used to avoid name conflicts in `define` and `paste` calls. Namespaces can be automatically created by `include` functions.

Namespaces can be nested. Relative path is always used in other functions' calls.

#### `paste[id from]`

Copies body of a definition with ID `id` to where the function is called. Parameter `from` selects which namespace to use (by default it's empty, which means current namespace is used). Parameter `from` is relative to the current location. Use `/` to access nested namespaces.

## Functions - examples

#### Doctype

File `index.shp` (entry point)

```shp
@doctype
@doctype[#EXAMPLE]
```

Result

```html
<!DOCTYPE HTML>
<!DOCTYPE EXAMPLE>
```

#### General define / paste

File `index.shp` (entry point)

```shp
@define[#foo] {
  $p { Foo content }
}
@paste[#foo]
```

Result

```html
<p>Foo content</p>
```

#### General namespaces

Definitions from namespaces can be accessed in the following ways:

- Inside the namespace, then its ID is not required
- Outside the namespace with specifying its ID
- Inside another namespace with the same ID, not repeating the ID in the paste call

File `index.shp` (entry point)

```shp
@namespace[#bar] {
  @define[#foo] {
    $p { Foo content }
  }
  @paste[#foo]
}

@paste[#foo from bar]

@namespace[$bar] {
  @paste[#foo]
}
```

Result

```html
<p>Foo content</p>
<p>Foo content</p>
<p>Foo content</p>
```

#### Accessing nested namespaces

File `index.shp` (entry point)

```shp
@namespace[#outer] {
  @namespace[#inner] {
    @define[#nested] {
      $p { Nested content }
    }
  }
  @paste[#nested from inner]
}
@paste[#nested from 'outer/inner']
```

Result

```html
<p>Nested content</p>
<p>Nested content</p>
```

#### Simple definition include

File `index.shp` (entry point)

```shp
@include[file bar]
$p { Index was the entry point }
@paste[#foo]
```

File `bar.shp`

```shp
@define[#foo] {
  $p { But bar.shp content is included }
}
```

Result

```html
<p>Index was the entry point</p>
<p>But bar.shp content is included</p>
```

#### Simple content include

File `index.shp` (entry point)

```shp
@doctype
$html {
  $head {
    %meta[charset 'utf-8']
    @include[file 'brain']
    $title {Example}
  }
  $body
}
```

File `brain.shp`

```shp
$script[src 'lib/Domi.js']
$script[src 'lib/shp.js']
```

Result

```html
<!DOCTYPE HTML>
<html>
    <head>
        <meta charset 'utf-8'>
        <script src 'lib/Domi.js'></script>
        <script src 'lib/shp.js'></script>
        <title>Example</title>
    </head>
    <body>
    </body>
</html>
```

#### Nested include and directories

File `index.shp` (entry point)

```shp
@doctype
$html {
  $head {
    %meta[charset 'utf-8']
  }
  $body {
    $p {Index content}
    @include[file 'component/footer']
  }
}
```

File `component/footer.shp`

```shp
$footer {
  $p {This is a footer}
  @include[file copyright]
}
```

File `component/copyright.shp`

```shp
$p {Made by me, 2022}
```

Result

```html
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset 'utf-8'>
  </head>
  <body>
    <p>Index content</p>
    <footer>
      <p>This is a footer</p>
      <p>Made by me, 2022</p>
    </footer>
  </body>
</html>
```

#### Templates based design

Generally include is used to paste content or definitions into your entry point file.

However, there is an alternative approach. You can define the general tree structure in a template file and add paste statements there. Then, in your entry point file create definitions with content unique for each page. This completely removes the redundancy of the general HTML structure and common head contents.

File `index.shp` (entry point)

```shp
@include [template/general]
@define[#Body] {
  $div { Hello world! }
}
```

File `template/general.shp`

```shp
@doctype
$html {
  $head {
    %meta[charset 'utf-8']
    $title { Reusability! }
  }
  $body {
    $header { This is a header }
    @paste[#Body]
  }
}
```

Result

```html
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset 'utf-8'>
    <title> Reusability! </title>
  </head>
  <body>
    <header>This is a header</header>
    <div>Hello world!</div>
  </body>
</html>
```

