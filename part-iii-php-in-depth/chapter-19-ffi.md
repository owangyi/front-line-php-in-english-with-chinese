# CHAPTER 19

## FFI PHP has a rich ecosystem of extensions, and most of them can be installed using a simple pecl install … . Many of those extensions provide their functionality by integrating with third-party libraries. Take, for example, an extension like imagick: it's written in C and exposes the underlying ImageMagick library as functions to PHP. The imagick extension itself doesn't provide the image processing functionality; it only provides a bridge between PHP and ImageMagick.

FFI — "foreign function interface" in full — makes the process of exposing such under -

lying libraries "easier". I use quotes because you still need to understand how those libraries work under the hood, but you don't need to write and distribute a dedicated extension anymore. FFI makes this process easier because it allows you to write PHP where you'd otherwise had to implement an extension in C.

In other words: if the required libraries are present on your server or local development environment, you can install extension-like functionality by using composer and downloading only PHP code. You can integrate with any language, as long as it can compile to a shared library, which are .so files on Unix and Linux systems or .dll  files on Windows.To get a feeling of how FFI code would look, let's look at an example taken from the official FFI documentation page:

```php
$ffi = FFI=:cdef("

    typedef unsigned int time_t;

    typedef unsigned int suseconds_t;

 

    struct timeval {

        time_t      tv_sec;

        suseconds_t tv_usec;

    };

 

    struct timezone {

        int tz_minuteswest;

        int tz_dsttime;

    };

 

    int gettimeofday(struct timeval *tv, struct timezone *tz);    

", "libc.so.6");
$tv = $ffi=>new("struct timeval");
$tz = $ffi=>new("struct timezone");

```

var_dump($ffi=>gettimeofday(

    FFI=:addr($tv), 

    FFI=:addr($tz))

```php
);

var_dump($tv=>tv_sec);

var_dump($tz);

```

This short example already shows the complexity of implementing FFI: you need to load header definitions into the $ffi  variable, and use the exposed structs and functions from that variable. Furthermore, you can't just copy this code snippet and run it via a web request: FFI is only enabled by default in the CLI and the preloading script because of security reasons. Imagine if you'd be able to manipulate FFI code from a web request, and gain access to all system binaries and potentially exploit securi -

ty flaws within them. Mind you: you can enable FFI in web requests, but you should probably think twice before doing so. Finally, you need opcache enabled for FFI to work, so if you're running this script via the CLI, you'll have to enable opcache specifi -

cally since it's disabled by default over there.

Header Files Header files document what functionality is available in the shared library you're integrating with. It's common practice in C programming but unknown in PHP.

A header file as a list of definitions for structs and functions, without their actual implementation; something alike interfaces for classes. Unfortunately, PHP's FFI doesn't support all modern-day header syntax. So while the original header files are available for whatever library you want to integrate with, chances are you'll need to re-write them specifically for PHP to understand.

As you can see, there's more to FFI programming than writing simple PHP code. On the other hand, even though FFI isn't as performant as a compiled C extension — it has the overhead of having to parse the header files — it can offer a significant per -

formance improvement compared to implementing the same functionality directly in PHP. In summary: FFI has potential but isn't a plug-and-play solution.

That brings us to the question: what use cases are there for FFI? The first ones that come to mind are the CPU-heavy tasks that are way more efficient to do in low-lev-el languages such as C or Rust than in PHP. So I asked around the community who's using FFI, and there are indeed a handful of people using it. One example is to parse large data sets efficiently. There's also the use case of shipping extension-like code with composer.

Another interesting example is changing the PHP runtime itself so that you don't need to add the opening <?php  tag in your PHP files anymore. It's interesting to see how much becomes possible when PHP can talk to other languages directly. One more: 

there's a project created by Anthony Ferrara called php-compiler . It can compile (a limited set) of PHP code and generate a binary from that code; it's actually written in PHP using FFI.

Interested In More?

There's an interesting GitHub repository that lists examples of using FFI in PHP called gabrielrcouto/awesome-php-ffi .

Most FFI projects are still very young, though. FFI is supported as of PHP 7.4, so it was only a year old when this book was released. Overall, FFI isn't widely used yet. There's nothing wrong with that: it's a rather niche solution that not many PHP developers have to deal with. Still, FFI has potential, but it probably needs some polishing before it'll be widely adopted. So let's look forward to how it will evolve in the years to come!
