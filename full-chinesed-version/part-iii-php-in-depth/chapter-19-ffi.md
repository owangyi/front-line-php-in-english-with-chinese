# 第十九章

## FFI

PHP 有一个丰富的扩展生态系统，其中大多数可以使用简单的 pecl install … 安装。其中许多扩展通过与第三方库集成来提供其功能。例如，像 imagick 这样的扩展：它是用 C 编写的，并将底层的 ImageMagick 库作为函数暴露给 PHP。imagick 扩展本身不提供图像处理功能；它只提供 PHP 和 ImageMagick 之间的桥梁。

FFI——全称"foreign function interface"（外部函数接口）——使暴露这样的底层库的过程"更容易"。我使用引号是因为你仍然需要了解这些库在底层如何工作，但你不再需要编写和分发专用扩展。FFI 使这个过程更容易，因为它允许你在原本必须用 C 实现扩展的地方编写 PHP。

换句话说：如果所需的库存在于你的服务器或本地开发环境中，你可以通过使用 composer 并仅下载 PHP 代码来安装类似扩展的功能。你可以与任何语言集成，只要它可以编译为共享库，在 Unix 和 Linux 系统上是 .so 文件，在 Windows 上是 .dll 文件。为了感受 FFI 代码的样子，让我们看一个来自官方 FFI 文档页面的示例：

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

这个简短的示例已经显示了实现 FFI 的复杂性：你需要将头文件定义加载到 $ffi 变量中，并使用该变量暴露的结构和函数。此外，你不能只是复制此代码片段并通过 Web 请求运行它：由于安全原因，FFI 默认仅在 CLI 和预加载脚本中启用。想象一下，如果你能够从 Web 请求操作 FFI 代码，并获得对所有系统二进制文件的访问权限，并可能利用其中的安全

漏洞。请注意：你可以在 Web 请求中启用 FFI，但你可能应该三思而后行。最后，你需要启用 opcache 才能使 FFI 工作，所以如果你通过 CLI 运行此脚本，你必须专门启用 opcache，因为它在默认情况下是禁用的。

## 头文件

头文件记录了你要集成的共享库中可用的功能。这是 C 编程中的常见做法，但在 PHP 中不为人知。

头文件是结构和函数的定义列表，没有它们的实际实现；类似于类的接口。不幸的是，PHP 的 FFI 不支持所有现代头文件语法。所以虽然原始头文件可用于你想要集成的任何库，但你可能需要专门为 PHP 重写它们以便理解。

正如你所看到的，FFI 编程不仅仅是编写简单的 PHP 代码。另一方面，即使 FFI 不如编译的 C 扩展那样高性能——它必须解析头文件的开销——与直接在 PHP 中实现相同功能相比，它可以提供显著的性能

改进。总结：FFI 有潜力，但不是即插即用的解决方案。

这给我们带来了一个问题：FFI 有哪些用例？首先想到的是 CPU 密集型任务，在低级语言（如 C 或 Rust）中比在 PHP 中更高效。所以我询问了社区中谁在使用 FFI，确实有少数人在使用它。一个例子是高效解析大型数据集。还有通过 composer 提供类似扩展代码的用例。

另一个有趣的例子是更改 PHP 运行时本身，这样你就不再需要在 PHP 文件中添加开头的 <?php 标签。看到当 PHP 可以直接与其他语言对话时，有多少变得可能，这很有趣。还有一个：

有一个由 Anthony Ferrara 创建的项目，名为 php-compiler。它可以编译（有限集合的）PHP 代码并从该代码生成二进制文件；它实际上是用 PHP 使用 FFI 编写的。

## 想了解更多？

有一个有趣的 GitHub 仓库，列出了在 PHP 中使用 FFI 的示例，名为 gabrielrcouto/awesome-php-ffi。

不过，大多数 FFI 项目仍然非常年轻。FFI 从 PHP 7.4 开始支持，所以当这本书发布时，它只有一岁。总的来说，FFI 还没有被广泛使用。这没有什么问题：这是一个相当小众的解决方案，没有多少 PHP 开发人员必须处理。尽管如此，FFI 有潜力，但它可能需要在被广泛采用之前进行一些改进。所以让我们期待它在未来几年如何发展！

