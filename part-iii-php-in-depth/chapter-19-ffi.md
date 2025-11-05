# Chapter 19: FFI

PHP has a rich ecosystem of extensions, and most of them can be installed using

PHP 有一个丰富的扩展生态系统，其中大多数可以使用简单的 `pecl install …` 安装。许多这些扩展通过集成第三方库来提供它们的功能。例如，像 `imagick` 这样的扩展：它是用 C 编写的，并将底层的 ImageMagick 库作为函数暴露给 PHP。`imagick` 扩展本身不提供图像处理功能；它只提供 PHP 和 ImageMagick 之间的桥梁。

a simple pecl install …. Many of those extensions provide their functionality by

FFI——全称"foreign function interface"（外部函数接口）——使暴露此类底层库的过程"更容易"。我使用引号是因为你仍然需要了解这些库在底层如何工作，但你不再需要编写和分发专用的扩展。FFI 使这个过程更容易，因为它允许你在其他地方必须用 C 实现扩展的地方编写 PHP。

integrating with third-party libraries. Take, for example, an extension like imagick: it's

换句话说：如果所需的库存在于你的服务器或本地开发环境中，你可以通过使用 composer 并仅下载 PHP 代码来安装类似扩展的功能。你可以与任何语言集成，只要它可以编译为共享库，这些库在 Unix 和 Linux 系统上是 `.so` 文件，在 Windows 上是 `.dll` 文件。

written in C and exposes the underlying ImageMagick library as functions to PHP. The

要了解 FFI 代码的样子，让我们看一个来自官方 FFI 文档页面的示例：

imagick extension itself doesn't provide the image processing functionality; it only

这个简短的例子已经显示了实现 FFI 的复杂性：你需要将头文件定义加载到 `$ffi` 变量中，并使用从该变量暴露的结构和函数。此外，你不能只是复制这个代码片段并通过 Web 请求运行它：由于安全原因，FFI 默认只在 CLI 和预加载脚本中启用。想象一下，如果你能够从 Web 请求操作 FFI 代码，并获得对所有系统二进制文件的访问权限，并可能利用其中的安全漏洞。请注意：你可以在 Web 请求中启用 FFI，但在这样做之前，你可能应该三思而后行。最后，你需要为 FFI 工作启用 opcache，所以如果你通过 CLI 运行此脚本，你必须特别启用 opcache，因为它在默认情况下在那里是禁用的。

provides a bridge between PHP and ImageMagick.

头文件记录了你正在集成的共享库中可用的功能。这在 C 编程中是常见做法，但在 PHP 中是未知的。

FFI — "foreign function interface" in full — makes the process of exposing such under-

头文件作为结构和函数的定义列表，没有它们的实际实现；类似于类的接口。不幸的是，PHP 的 FFI 不支持所有现代头文件语法。所以虽然原始头文件可用于你想要集成的任何库，但你可能需要专门为 PHP 重写它们以便理解。

lying libraries "easier". I use quotes because you still need to understand how those

正如你所看到的，FFI 编程不仅仅是编写简单的 PHP 代码。另一方面，即使 FFI 不如编译的 C 扩展那样高性能——它必须解析头文件的开销——它仍然可以提供比直接在 PHP 中实现相同功能的显著性能改进。总之：FFI 有潜力，但不是即插即用的解决方案。

libraries work under the hood, but you don't need to write and distribute a dedicated

这给我们带来了一个问题：FFI 有哪些用例？首先想到的是 CPU 密集型任务，在低级语言（如 C 或 Rust）中比在 PHP 中更高效。所以我询问了社区中使用 FFI 的人，确实有一些人在使用它。一个例子是高效解析大型数据集。还有通过 composer 交付类似扩展代码的用例。

extension anymore. FFI makes this process easier because it allows you to write PHP

另一个有趣的例子是更改 PHP 运行时本身，这样你不再需要在 PHP 文件中添加开头的 `<?php` 标签。看看当 PHP 可以直接与其他语言对话时，有多少变得可能，这很有趣。还有一个：有一个由 Anthony Ferrara 创建的项目，名为 `php-compiler`。它可以编译（有限集的）PHP 代码并从该代码生成二进制文件；它实际上是用 PHP 使用 FFI 编写的。

where you'd otherwise had to implement an extension in C.

有一个有趣的 GitHub 仓库列出了在 PHP 中使用 FFI 的示例，名为 `gabrielrcouto/awesome-php-ffi`。

In other words: if the required libraries are present on your server or local develop-

不过，大多数 FFI 项目仍然非常年轻。FFI 从 PHP 7.4 开始支持，所以当这本书发布时它只有一岁。总的来说，FFI 还没有被广泛使用。这没有什么错：这是一个相当小众的解决方案，没有多少 PHP 开发者必须处理它。尽管如此，FFI 有潜力，但在它被广泛采用之前可能需要一些改进。所以让我们期待它未来几年的发展！

ment environment, you can install extension-like functionality by using composer and

downloading only PHP code. You can integrate with any language, as long as it can

compile to a shared library, which are .so files on Unix and Linux systems or .dll files

on Windows.

216

To get a feeling of how FFI code would look, let's look at an example taken from the

official FFI documentation page:

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

var_dump($ffi=>gettimeofday(

FFI=:addr($tv),

FFI=:addr($tz))

);

var_dump($tv=>tv_sec);

var_dump($tz);

Chapter 19 - FFI

This short example already shows the complexity of implementing FFI: you need to

load header definitions into the $ffi variable, and use the exposed structs and func-

tions from that variable. Furthermore, you can't just copy this code snippet and run it

via a web request: FFI is only enabled by default in the CLI and the preloading script

because of security reasons. Imagine if you'd be able to manipulate FFI code from a

web request, and gain access to all system binaries and potentially exploit securi-

ty flaws within them. Mind you: you can enable FFI in web requests, but you should

probably think twice before doing so. Finally, you need opcache enabled for FFI to

work, so if you're running this script via the CLI, you'll have to enable opcache specifi-

cally since it's disabled by default over there.

Header Files

Header files document what functionality is available in the shared library you're

integrating with. It's common practice in C programming but unknown in PHP.

A header file as a list of definitions for structs and functions, without their actual

implementation; something alike interfaces for classes. Unfortunately, PHP's FFI

doesn't support all modern-day header syntax. So while the original header files

are available for whatever library you want to integrate with, chances are you'll

need to re-write them specifically for PHP to understand.

As you can see, there's more to FFI programming than writing simple PHP code. On

the other hand, even though FFI isn't as performant as a compiled C extension — it

has the overhead of having to parse the header files — it can offer a significant per-

formance improvement compared to implementing the same functionality directly in

PHP. In summary: FFI has potential but isn't a plug-and-play solution.

That brings us to the question: what use cases are there for FFI? The first ones that

come to mind are the CPU-heavy tasks that are way more efficient to do in low-lev-

218

el languages such as C or Rust than in PHP. So I asked around the community who's

using FFI, and there are indeed a handful of people using it. One example is to parse

large data sets efficiently. There's also the use case of shipping extension-like code

with composer.

Another interesting example is changing the PHP runtime itself so that you don't need

to add the opening <?php tag in your PHP files anymore. It's interesting to see how

much becomes possible when PHP can talk to other languages directly. One more:

there's a project created by Anthony Ferrara called php-compiler. It can compile (a

limited set) of PHP code and generate a binary from that code; it's actually written in

PHP using FFI.

Interested In More?

There's an interesting GitHub repository that lists examples of using FFI in PHP

called gabrielrcouto/awesome-php-ffi.

Most FFI projects are still very young, though. FFI is supported as of PHP 7.4, so it was

only a year old when this book was released. Overall, FFI isn't widely used yet. There's

nothing wrong with that: it's a rather niche solution that not many PHP developers

have to deal with. Still, FFI has potential, but it probably needs some polishing before

it'll be widely adopted. So let's look forward to how it will evolve in the years to come!

