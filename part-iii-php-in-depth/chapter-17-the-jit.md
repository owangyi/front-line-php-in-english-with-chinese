# CHAPTER 17

## THE JIT

There's been a lot of hype over the JIT in PHP 8. Some say it will revolutionize the PHP landscape. In this chapter we'll discuss what the JIT is about, how it can significantly impact PHP's performance, and look at some real-life benchmarks.

PHP 8 中的 JIT 有很多炒作。有人说它将彻底改变 PHP 的格局。在本章中，我们将讨论 JIT 是什么，它如何显著影响 PHP 的性能，并查看一些实际基准测试。

## What is the JIT?

First things first: " JIT" stands for "just in time". Its full name is "the just in time compiler". You might remember that, back in chapter 4, I explained the difference between a compiled language and an interpreted one: PHP falls in the latter category. So, where is this compiler coming from? Well, in fact: PHP has a compiler, but it's not a one like you'd see in compiled languages: there is no standalone step to run it, and it doesn't generate a binary. The compiler is part of PHP's runtime engine: PHP code still needs to be compiled — translated — to machine code; it just happens on the fly when running PHP code.

首先："JIT"代表"just in time"（即时）。它的全名是"即时编译器"。你可能还记得，在第 4 章中，我解释了编译语言和解释语言之间的区别：PHP 属于后者。那么，这个编译器是从哪里来的？嗯，事实上：PHP 有一个编译器，但它不像你在编译语言中看到的那样：没有独立的步骤来运行它，它不会生成二进制文件。编译器是 PHP 运行时引擎的一部分：PHP 代码仍然需要被编译——翻译——为机器代码；它只是在运行 PHP 代码时即时发生。
> ⚠️ JIT 是编译并缓存机器码，Opcache 是缓存字节码


A JIT compiler takes advantage of an interpreted language like this: it looks at the code while running and tries to identify the so-called "hot parts" of that code (parts that are executed more often than others). The JIT will take that source code and compile it on the fly to a more optimized, machine-friendly blob of code, which can be run instead. Interestingly, this is only possible in interpreted languages because programs which are fully compiled beforehand can't change anymore.The mechanism that tries to identify hot parts is called a "monitor": it will look at the code, and monitor it while running. When it detects parts that are executed several times, it will mark them as "warm" or "hot". It can then compile the hot parts into optimized blobs of code. You can imagine there's a lot more complexity to this topic, but this book's goal isn't to explain the JIT compiler in depth. Instead, it's to teach you how and when to use it in PHP.

JIT 编译器利用像这样的解释语言：它在运行时查看代码并尝试识别所谓的"热点"（比其他部分执行更频繁的部分）。JIT 将获取该源代码并即时编译为更优化的、对机器友好的代码块，可以运行它。有趣的是，这只能在解释语言中实现，因为完全预先编译的程序无法再改变。尝试识别热点的机制称为"监视器"：它将查看代码，并在运行时监视它。当它检测到执行多次的部分时，它会将它们标记为"温"或"热"。然后它可以将热点编译为优化的代码块。你可以想象这个话题还有很多复杂性，但本书的目标不是深入解释 JIT 编译器。相反，它是教你如何在 PHP 中使用它以及何时使用它。

While this might sound great in theory, there are a few sidenotes to be made. First of all: monitoring code and generating JIT'ed code also comes with a performance cost. Luckily the benefits gained from the JIT outweigh that cost. At least, in some cases.

虽然这在理论上听起来很棒，但有一些注意事项。首先：监视代码和生成 JIT 代码也会带来性能成本。幸运的是，从 JIT 获得的好处超过了这个成本。至少，在某些情况下。

The second problem is more important: there aren't many hot parts to optimise in a regular MVC application serving web requests. When the JIT was still in its early days, a popular example was shared within the PHP community. It showed a fractal being generated with and without the JIT. The JIT'ed version was significant — tens times — faster. But let's be honest: we're very rarely generating fractal images in our PHP applications.

第二个问题更重要：在服务 Web 请求的常规 MVC 应用程序中，没有多少热点可以优化。当 JIT 还处于早期阶段时，PHP 社区中分享了一个流行的例子。它显示了使用和不使用 JIT 生成的分形。JIT 版本显著——十倍——更快。但让我们诚实地说：我们在 PHP 应用程序中很少生成分形图像。

Even on the framework level, there's very little code that benefits from an optimized JIT'ed version. The main performance bottleneck in web applications isn't the code itself; it's I/O operations like sending and receive requests, reading data from the file system, or communicating with a database server.

即使在框架级别，也很少有代码从优化的 JIT 版本中受益。Web 应用程序中的主要性能瓶颈不是代码本身；它是 I/O 操作，如发送和接收请求、从文件系统读取数据，或与数据库服务器通信。

We're speculating about the JIT's performance at this point. Let's look at some real-life benchmarks instead. I took a Laravel project with its production database and decided to benchmark it.

我们此时正在推测 JIT 的性能。让我们看看一些实际的基准测试。我拿了一个 Laravel 项目及其生产数据库，并决定对其进行基准测试。

## Real -Life Benchmarks
Let's set the scene first. These benchmarks were run on my local machine. Consequently, they don't say anything about absolute performance gains; here, I'm only interested in making conclusions about the relative impact the JIT has on real-life code.

让我们先设置场景。这些基准测试在我的本地机器上运行。因此，保证机器不会影响性能测试结果；在这里，我只对
JIT 对实际代码的相对影响做出结论感兴趣。

I'll be running PHP FPM, configured to spawn 20 child processes, and I'll always make sure to only run 20 concurrent requests at once, to eliminate any extra performance hits on the FPM level. Sending these requests is done using the following command, with ApacheBench:

我将运行 PHP FPM，配置为生成 20 个子进程，并且我将始终确保一次只运行 20 个并发请求，以消除 FPM 级别的任何额外性能影响。发送这些请求是使用以下命令完成的，

```
ab -n 100 -c 20 -l localhost:8000 
```

## JIT Setup
With the project in place, let's configure the JIT itself. The JIT is enabled by specifying the opcache.jit_buffer_size  option in php.ini . If this directive is excluded, the default value is set to 0, and the JIT won't run.

项目就位后，让我们配置 JIT 本身。JIT 通过在 php.ini 中指定 opcache.jit_buffer_size 选项来启用。如果排除此指令，默认值设置为 0，JIT 将不会运行。
```
opcache.jit_buffer_size=100M 
```
You'll also want to set a JIT mode, which will determine how the JIT will monitor and react to hot parts of your code. You'll need to use the opcache.jit  option. Its default is set to tracing , but you can set it to function  as well:

你还想设置一个 JIT 模式，这将确定 JIT 如何监视和响应代码的热点。你需要使用 opcache.jit 选项。它的默认值设置为 tracing，但你也可以将其设置为 function：
```
opcache.jit=function
; opcache.jit=tracing
```
The tracing  or function  mode will determine how the JIT will work. The difference is that the function  JIT will only monitor and compile code within the context of a single function, while the tracing  JIT can look across those boundaries. In our real-life benchmarks, I'll compare both modes with each other. So let's start benchmarking!

tracing 或 function 模式将确定 JIT 如何工作。区别在于 function JIT 只会在单个函数的上下文中监视和编译代码，而 tracing JIT 可以跨越这些边界。在我们的实际基准测试中，我将比较两种模式。所以让我们开始基准测试！

## Establishing a Baseline
First, it's best to establish whether the JIT is working properly or not. We know from the RFC that it does have a significant impact on calculating a fractal. So let's start with that example. I copied the mandelbrot example from the RFC and accessed it via the same HTTP application I'll run the next benchmarks on:

首先，最好确定 JIT 是否正常工作。我们从 RFC 中知道它对计算分形有显著影响。所以让我们从那个例子开始。我从 RFC 复制了 mandelbrot 示例，并通过我将运行下一个基准测试的相同 HTTP 应用程序访问它：

```php
public function index()

{

    for ($y = -39; $y < 39; $y=+) {

        printf("\n");

        for ($x = -39; $x < 39; $x=+) {
            $i = $this=>mandelbrot(
            $x / 40.0,
            $y / 40.0

            );

            if ($i == 0) {

                printf("*");

            } else {

                printf(" ");

            }

        }

    }

    printf("\n");

}

private function mandelbrot($x, $y)
{
    $cr = $y - 0.5;
    $ci = $x;
    $zi = 0.0;
    $zr = 0.0;
    $i = 0;

    while (1) {
        $i=+;
        $temp = $zr * $zi;
        $zr2 = $zr * $zr;
        $zi2 = $zi * $zi;
        $zr = $zr2 - $zi2 + $cr;
        $zi = $temp + $temp + $ci;

        if ($zi2 + $zr2 > 16) {

            return $i;

        }

        if ($i > 5000) {

            return 0;

        }

    }
}
```

After running ab for a few hundred requests, we can see the results:

运行 ab 几百个请求后，我们可以看到结果：
```
                                      requests/second (more is better)

Mandelbrot without JIT                                            3.60 Mandelbrot with tracing JIT                                      41.36 Great, it looks like the JIT is working! There's even a ten times performance increase!

```
If you want to verify whether the JIT is running, you can use opcache_get_status() , it has a jit entry which lists all relevant information:

如果你想验证 JIT 是否正在运行，你可以使用 opcache_get_status()，它有一个 jit 条目，列出了所有相关信息：

```php
print_r(opcache_get_status()['jit']);

// array:7 [

//   "enabled" => true

//   "on" => true

//   "kind" => 5

//   "opt_level" => 4

//   "opt_flags" => 6

//   "buffer_size" => 104857584

//   "buffer_free" => 104478688

// ]
```
Having verified it works as expected, let's move on to our first real-life comparison. 
We're going to compare running our code without the JIT, with the function JIT, and the tracing JIT, both are using 100MB of memory. The page we're going to benchmark shows an overview of posts, so there's some recursion happening. We're also touching several core parts of Laravel: routing, the dependency container, as well as the ORM layer.

验证它按预期工作后，让我们继续我们的第一个实际比较。
我们将比较在没有 JIT、使用 function JIT 和使用 tracing JIT 的情况下运行我们的代码，两者都使用 100MB 内存。我们将进行基准测试的页面显示帖子概览，所以有一些递归发生。我们还接触了 Laravel 的几个核心部分：路由、依赖容器以及 ORM 层。
```
                                      requests/second (more is better)

No JIT                                                           63.56 Function JIT                                                              66.32 Tracing JIT                                                              69.45
```
Here we see the results: enabling the JIT only has a slight improvement. In fact, 
running the benchmarks repeatedly, the results differ slightly every time: I've even seen cases where a JIT enabled run performs worse than the non JIT'ed version. 
Before drawing conclusions, let's bump the memory buffer limit. We'll give the JIT a little more room to breathe with 500MB of memory instead of 100MB.

这里我们看到结果：启用 JIT 只有轻微的改进。事实上，重复运行基准测试，结果每次都略有不同：我甚至看到过 JIT 启用的运行比非 JIT 版本表现更差的情况。在得出结论之前，让我们提高内存缓冲区限制。我们将给 JIT 更多的呼吸空间，使用 500MB 内存而不是 100MB。

```

                                      requests/second (more is better)

No JIT                                                           71.69 Function JIT                                                              72.82 Tracing JIT                                                              70.11
```
Here we have a case of the JIT performing worse. Like I said at the beginning of this chapter: I want to measure the relative impact of the JIT on real-life web projects. It's clear from these tests that sometimes there might be benefits, but it's in no way as noticeable as the fractal example we started with. I admit I'm not surprised by that. 

这里我们有一个 JIT 表现更差的情况。就像我在本章开头说的：我想测量 JIT 对实际 Web 项目的相对影响。从这些测试中可以清楚地看出，有时可能会有好处，但绝不像我们开始时的分形示例那样明显。我承认我并不感到惊讶。

Like I wrote before: there's very little hot code to be optimised in real-life applications. 

就像我之前写的：在实际应用程序中，很少有热点代码可以优化。

We're only rarely doing fractal-like computations.

我们很少做类似分形的计算。

So am I saying there's no need for the JIT? Not quite. I think the JIT can open up new areas for PHP: areas where complex computations do benefit from JIT'ed code. I'm thinking about machine learning and parsers, stuff like that. The JIT might give the PHP community opportunities that didn't exist yet, but it's unclear to say anything with certainty at this point.For example, there's a package called nikic/php-parser  - a PHP implementation that can take PHP code and parse into structured data. This package is actually used by static analysis tools like Psalm, and it turns out this one does benefit a lot from the JIT. 

所以我说不需要 JIT 吗？不完全是这样。我认为 JIT 可以为 PHP 开辟新领域：复杂计算确实从 JIT 代码中受益的领域。我在考虑机器学习和解析器之类的东西。JIT 可能为 PHP 社区提供尚不存在的机会，但在这一点上，不确定地说任何事情。例如，有一个名为 nikic/php-parser 的包——一个 PHP 实现，可以获取 PHP 代码并解析为结构化数据。这个包实际上被像 Psalm 这样的静态分析工具使用，事实证明这个包确实从 JIT 中受益匪浅。

So even today, there's already advantages, just not when running a web application.

所以即使在今天，已经有优势了，只是在运行 Web 应用程序时没有。

## A Complexity to Maintain
Adding the JIT to PHP's core also comes with the added maintenance cost. Because the JIT generates machine code, you can imagine it's complex material for a higher level programmer to understand. Say there is a bug in the JIT compiler. For that, you need a developer who knows how to fix it. In this JIT's case, Dmitry Stogov did most programming on it, and there's only a handful of people who understand how it works.

将 JIT 添加到 PHP 核心也带来了额外的维护成本。因为 JIT 生成机器代码，你可以想象对于高级程序员来说，理解它是复杂的材料。假设 JIT 编译器中有一个 bug。为此，你需要一个知道如何修复它的开发人员。在这个 JIT 的情况下，Dmitry Stogov 在它上面做了大部分编程，只有少数人理解它是如何工作的。


With just a few people being able to maintain such a codebase today, the question whether the JIT compiler can be maintained properly seems justified. Of course, people can learn how the compiler works, but it is a complex matter nevertheless. 
I don't think this should be a reason to ditch the JIT, but the cost of maintenance should still be carefully considered. In the first instance, by the ones maintaining the code and the userland community, who should also be aware that some bugfixes or version updates might take longer than what we're used to right now.

由于今天只有少数人能够维护这样的代码库，JIT 编译器是否可以正确维护的问题似乎是合理的。当然，人们可以学习编译器如何工作，但这仍然是一个复杂的问题。
我不认为这应该是放弃 JIT 的理由，但维护成本仍然应该仔细考虑。首先，由维护代码的人和用户社区，他们也应该意识到一些 bug 修复或版本更新可能需要比我们现在习惯的更长的时间。


## Do You Want It?

If you think that the JIT offers little short-term benefits for your web applications, I'd say you're right. It's clear that its impact will be minimal at best.

如果你认为 JIT 为你的 Web 应用程序提供的短期好处很少，我会说你是对的。很明显，它的影响充其量是最小的。

Despite that, we should remember that the JIT can open many possibilities for PHP to grow, both as a web language and a more generally purposed language. So the question that needs answering: is this possibly a bright future worth the investment today?

尽管如此，我们应该记住，JIT 可以为 PHP 的成长开辟许多可能性，无论是作为 Web 语言还是更通用的语言。所以需要回答的问题：这可能是值得今天投资的光明未来吗？

Time will tell.

时间会证明一切