# Chapter 22: Async PHP

When discussing the MVC pattern, we looked at why it was a good fit for PHP, espe-

在讨论 MVC 模式时，我们研究了为什么它适合 PHP，特别是因为 PHP 有一个非常干净的请求/响应周期。每次新请求到达时，一个新进程启动并从零开始启动我们的 PHP 应用程序。这个特性使 PHP 如此容易上手：你不需要任何编译器，你不需要处理跨请求的共享状态或担心内存管理；它超级简单。

cially since PHP has a very clean request/response cycle. Every time a new request

不过，简单并不总是首选。PHP 中有一个社区在过去几年中越来越受欢迎：异步社区。在这本书中提到他们是值得的，因为最近有越来越多的异步 PHP 用例。现代 PHP 不仅用于为博客或小公司网站提供支持；它还用于构建大规模的大型 Web 应用程序，在某些情况下，异步会带来显著价值。

arrives, a new process starts and boots our PHP application from scratch. This char-

首先明确：我无法在本章中深入解释异步编程。解释异步需要一本书。本章的目标是让你了解 PHP 的选项。所以我假设你知道一些异步相关的词汇。如果不是这样，也不用担心，它仍然会是一个有趣的阅读，但如果你对这个话题感兴趣，你可能需要做一些后续研究。在这种情况下，我建议你看看 JavaScript 社区，它比其他语言更拥抱异步编程，并且有很好的资源来学习异步思维。

acteristic makes PHP so easy to start with: you don't need any compiler, you don't

通过"异步 PHP"，我们指的是一个 PHP 进程可以同时处理多个事情。你可以使用线程或创建子进程，每个都专门用于单个任务。反过来，父进程将监控和管理所有这些子进程。例如，你可以为每个传入的请求创建一个子进程，并从父进程共享已加载和启动的框架，而不是在每个请求上从头启动它。

need to deal with shared state across requests or worry about memory management;

异步不仅仅是管理子进程，尽管。想想处理 I/O，比如读取文件或与外部服务通信。与其执行数据库查询并等待结果再执行下一个，你可以并行执行所有查询。假设你有十个查询，每个需要一秒钟执行；你可以在一秒钟内运行所有查询，而不是十秒。

it's super simple.

简而言之，如果使用得当，异步编程可以显著提高性能。

Simplicity isn't always preferred, though. There's a community within PHP that has

不过，大多数 MVC 框架没有针对异步思维进行优化：它们假设每次新请求到达时都必须从头启动。反过来，它们试图通过缓存和将配置编译为优化的生产就绪版本来优化该过程的部分。你可能本能地认为，如果你能够跳过框架的"启动阶段"，你会看到巨大的性能改进；但事实并非如此。

started to grow in popularity over the years: the async community. It's worth men-

你看，拥有"共享应用程序状态"并在 PHP 内并行处理请求不会有显著差异：你的 Web 服务器已经在运行多个进程来并行处理请求。除此之外，你可以使用预加载来让应用程序在内存中启动并准备就绪。最大的性能提升来自异步处理 I/O，大多数框架没有针对此进行优化。它们不是用异步思维构建的。这很好，因为异步 PHP 增加了一层对许多项目来说过度的复杂性。

tioning them in this book because there are more and more use cases for async PHP

考虑到这一点，你不应该期望通过简单地将 MVC 框架和异步框架（如 Amp 或 ReactPHP）结合起来就能获得突破性的性能提升——还有更多。异步有比平均 MVC 应用程序更有趣的用例。

lately. Modern PHP isn't only used to power blogs or small company websites; it's also

想想需要做大量实时重型计算的复杂 API。当我询问社区中有异步 PHP 现实用例的人时，有人告诉我他们使用 Swoole 运行他们的 API。Swoole 使他们能够在进程之间静态缓存数据以减少数据库 I/O，并并行执行复杂计算。总的来说，他们能够每秒服务 8000 个请求，而不是 600 个。

used to build large web applications at scale, and there are cases where async adds

我刚才提到了 Swoole，还谈到了 Amp（全称 Amphp）和 ReactPHP。这是今天使用的三个最流行的异步框架。Amp 和 ReactPHP 是用 PHP 本身实现的。你可以在项目中使用 composer 下载它们，你就可以开始了。另一方面，Swoole 是一个 PHP 扩展，你必须安装在系统上。虽然 ReactPHP 将自己描述为"事件驱动、非阻塞 I/O with PHP"的框架；Swoole 是"基于协程的异步 PHP 编程框架"。

significant value.

除了完整的异步框架之外，还有流行的 Guzzle HTTP 库，它可以并行执行 HTTP 请求。这是一种更简单和隔离的异步编程方法，但也有几个用例。假设你正在从分页 API 加载数据；你可以一次加载几页，而不是一页一页地加载。

To be clear upfront: I won't be able to explain async programming in depth in this

每个框架都有其目标受众和需求；所有都是今天在生产中使用的流行选择。

chapter. Explaining async requires a book on its own. The goal of this chapter is to let

我遇到的另一个现实例子是一个定期使用 AWS Lambda 发送 100,000 个推送通知的平台。与其生成 100,000 个 Lambda，他们将数据分块成 500 个组，并并行将每个组发送到总共 200 个 Lambda。他们使用 Guzzle 并行执行 200 个 HTTP 请求，并等待它们全部完成。反过来，每个 Lambda 也会并行发送 500 个推送通知，并在不到一分钟内完成。总的来说，由于异步编程，发送 100,000 个推送通知需要 2 分钟。

you know about the options out there for PHP. So I'll assume you know some async

人们有时将 PHP 与 NodeJS 进行比较，并提到它缺乏异步能力，但事实恰恰相反。PHP 中有很多异步编程选项。它们今天在各种用例中用于生产。PHP 与 JavaScript 的不同之处在于它没有内置的异步编程支持，如 async、await 或 promises。有人有兴趣在 PHP 的核心中添加 libuv，这是为 Node 的异步能力提供支持的相同库。还没有尝试集成它，但 PHP 很可能有一天会有一个内置的异步引擎。

related vocabulary. No worries if that's not the case though, it'll still be an interesting

在那之前，已经有一些很好的、经过实战测试的解决方案可以在今天使用。

read, but you probably will need to do some follow-up research if you're interested in

the topic. In that case, I'd advise you to look at the JavaScript community, which has

embraced async programming like no other language and has great resources to learn

the async mindset.

232

What's Async?

With "async PHP" we mean that one PHP process can handle several things at once.

You can use threads or create child processes, each dedicated to a single task. The

parent process, in turn, will monitor and manage all those children. For example, you

could create a child process for every request that comes in and share the loaded and

booted framework from the parent process instead of booting it from scratch on every

request.

Async is more than managing child processes, though. Think of dealing with I/O, such

as reading files or communicating with external services. Instead of performing a

database query and waiting for the result before executing the next one, you could

execute all your queries in parallel. Say you have ten queries that each take a second

to execute; you could potentially run all of them in one second instead of ten.

In short, async programming can boost performance significantly if used correctly.

Most MVC frameworks aren't optimised for the async mindset though: they assume

they'll have to boot from scratch every time a new request comes in. In turn, they try

to optimise parts of that process with caching and by compiling configuration into an

optimised production-ready version. You might instinctively think that if you're able to

skip the "boot phase" of your framework, you'd see massive performance improve-

ments; that's not entirely the case, though.

You see, having a "shared application state" and handling requests in parallel within

PHP wouldn't make a significant difference: your webserver is already running several

processes to serve requests in parallel. On top of that, you could use preloading to

have the application booted and ready in memory. The biggest performance win

comes from handling I/O asynchronously, which most frameworks aren't optimised

to do. They aren't built with the async mentality. That's fine since async PHP adds a

layer of complexity that's overkill for many projects.

Chapter 22 - Async PHP

Given that, you shouldn't expect groundbreaking performance gains by simply com-

bining an MVC framework and an async framework like Amp or ReactPHP - there's

more to it than that. There are more interesting use cases for async than the average

MVC application.

Think about complex APIs that need to do lots of realtime heavy calculations. When

I asked around the community for people who had real-life use cases for async PHP,

someone told me they used Swoole to run their API. Swoole enabled them to cache

data statically across processes to reduce database I/O and do complex computations

in parallel. All in all, they were able to serve 8000 requests per second instead of 600.

Async Frameworks

I mentioned Swoole just now and also talked about Amp (Amphp in full) and Re-

actPHP. Those are the three most popular async frameworks used today. Amp

and ReactPHP are implemented in PHP itself. You can download them in your

project with composer, and you're set. Swoole, on the other hand, is a PHP ex-

tension you'll have to install on your system. While ReactPHP describes itself as

a framework for "Event-driven, non-blocking I/O with PHP"; Swoole is a "Corou-

tine based Async PHP Programming Framework".

Besides full-blown async frameworks, there's also the popular Guzzle HTTP

library, which can perform HTTP requests in parallel. This is a much simpler and

isolated approach to async programming, but there are several use cases for it

as well. Say you're loading data from a paginated API; you could potentially load

several pages at once instead of loading them one by one.

Each framework has its target audience with its own needs; all are popular

choices and used in production today.

234

Another real-life example that I came across was a platform that regularly sent

out 100,000 push notifications using AWS Lambda. Instead of spawning 100,000

Lambdas, they chunked the data into groups of 500 and sent each group in parallel to

200 Lambdas in total. They used Guzzle to perform 200 HTTP requests in parallel and

waited for all of them to finish. Each Lambda in turn, would send the 500 push notifi-

cations in parallel as well and finished in under a minute. All in all, it took 2 minutes to

send out 100,000 push notifications, thanks to async programming.

People sometimes compare PHP to NodeJS and mention its lack of async capabilities,

but the opposite is true. There are lots of options for async programming in PHP. They

are used in production today for a variety of use cases. PHP differs with JavaScript in

that it has no built-in support for async programming such as async, await or promis-

es. There has been interest to add libuv in PHP's core, which is the same library that

powers Node's asynchronous capabilities. There haven't been any attempts to inte-

grate it, but chances are PHP will have a built-in async engine one day.

Until then, there are already great and battle-tested solutions out there that can be

used today.

235

