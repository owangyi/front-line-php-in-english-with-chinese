# CHAPTER 22

## ASYNC PHP When discussing the MVC pattern, we looked at why it was a good fit for PHP, espe -

cially since PHP has a very clean request/response cycle. Every time a new request arrives, a new process starts and boots our PHP application from scratch. This char -

```php
acteristic makes PHP so easy to start with: you don't need any compiler, you don't need to deal with shared state across requests or worry about memory management; 

```

it's super simple.

Simplicity isn't always preferred, though. There's a community within PHP that has started to grow in popularity over the years: the async community. It's worth men -

tioning them in this book because there are more and more use cases for async PHP lately. Modern PHP isn't only used to power blogs or small company websites; it's also used to build large web applications at scale, and there are cases where async adds significant value.

To be clear upfront: I won't be able to explain async programming in depth in this chapter. Explaining async requires a book on its own. The goal of this chapter is to let you know about the options out there for PHP. So I'll assume you know some async related vocabulary. No worries if that's not the case though, it'll still be an interesting read, but you probably will need to do some follow-up research if you're interested in the topic. In that case, I'd advise you to look at the JavaScript community, which has embraced async programming like no other language and has great resources to learn the async mindset.What's Async?

With "async PHP" we mean that one PHP process can handle several things at once. 

You can use threads or create child processes, each dedicated to a single task. The parent process, in turn, will monitor and manage all those children. For example, you could create a child process for every request that comes in and share the loaded and booted framework from the parent process instead of booting it from scratch on every request.

Async is more than managing child processes, though. Think of dealing with I/O, such as reading files or communicating with external services. Instead of performing a database query and waiting for the result before executing the next one, you could execute all your queries in parallel. Say you have ten queries that each take a second to execute; you could potentially run all of them in one second instead of ten.

In short, async programming can boost performance significantly if used correctly.

Most MVC frameworks aren't optimised for the async mindset though: they assume they'll have to boot from scratch every time a new request comes in. In turn, they try to optimise parts of that process with caching and by compiling configuration into an optimised production-ready version. You might instinctively think that if you're able to skip the "boot phase" of your framework, you'd see massive performance improvements; that's not entirely the case, though.

You see, having a "shared application state" and handling requests in parallel within PHP wouldn't make a significant difference: your webserver is already running several processes to serve requests in parallel. On top of that, you could use preloading to have the application booted and ready in memory. The biggest performance win comes from handling I/O asynchronously, which most frameworks aren't optimised to do. They aren't built with the async mentality. That's fine since async PHP adds a layer of complexity that's overkill for many projects.

Given that, you shouldn't expect groundbreaking performance gains by simply combining an MVC framework and an async framework like Amp or ReactPHP - there's more to it than that. There are more interesting use cases for async than the average MVC application.

Think about complex APIs that need to do lots of realtime heavy calculations. When I asked around the community for people who had real-life use cases for async PHP, 

someone told me they used Swoole to run their API. Swoole enabled them to cache data statically across processes to reduce database I/O and do complex computations in parallel. All in all, they were able to serve 8000 requests per second instead of 600.

Async Frameworks I mentioned Swoole just now and also talked about Amp (Amphp in full) and ReactPHP. Those are the three most popular async frameworks used today. Amp and ReactPHP are implemented in PHP itself. You can download them in your project with composer, and you're set. Swoole, on the other hand, is a PHP ex -

tension you'll have to install on your system. While ReactPHP describes itself as a framework for "Event-driven, non-blocking I/O with PHP"; Swoole is a "Corou -

tine based Async PHP Programming Framework".

Besides full-blown async frameworks, there's also the popular Guzzle HTTP library, which can perform HTTP requests in parallel. This is a much simpler and isolated approach to async programming, but there are several use cases for it as well. Say you're loading data from a paginated API; you could potentially load several pages at once instead of loading them one by one.

Each framework has its target audience with its own needs; all are popular choices and used in production today.Another real-life example that I came across was a platform that regularly sent out 100,000 push notifications using AWS Lambda. Instead of spawning 100,000 Lambdas, they chunked the data into groups of 500 and sent each group in parallel to 200 Lambdas in total. They used Guzzle to perform 200 HTTP requests in parallel and waited for all of them to finish. Each Lambda in turn, would send the 500 push notifi -

cations in parallel as well and finished in under a minute. All in all, it took 2 minutes to send out 100,000 push notifications, thanks to async programming.

People sometimes compare PHP to NodeJS and mention its lack of async capabilities, 

but the opposite is true. There are lots of options for async programming in PHP. They are used in production today for a variety of use cases. PHP differs with JavaScript in that it has no built-in support for async programming such as async , await  or promises. There has been interest to add libuv  in PHP's core, which is the same library that powers Node's asynchronous capabilities. There haven't been any attempts to integrate it, but chances are PHP will have a built-in async engine one day.

Until then, there are already great and battle-tested solutions out there that can be used today.
