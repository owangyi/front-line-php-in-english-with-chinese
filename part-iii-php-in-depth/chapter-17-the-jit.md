# CHAPTER 17

## THE JIT There's been a lot of hype over the JIT in PHP 8. Some say it will revolutionize the PHP landscape. In this chapter we'll discuss what the JIT is about, how it can significantly impact PHP's performance, and look at some real-life benchmarks.

What is the JIT?

First things first: " JIT" stands for "just in time". Its full name is "the just in time compil -

er". You might remember that, back in chapter 4, I explained the difference between a compiled language and an interpreted one: PHP falls in the latter category. So, where is this compiler coming from? Well, in fact: PHP has a compiler, but it's not a one like you'd see in compiled languages: there is no standalone step to run it, and it doesn't generate a binary. The compiler is part of PHP's runtime engine: PHP code still needs to be compiled — translated — to machine code; it just happens on the fly when running PHP code.

A JIT compiler takes advantage of an interpreted language like this: it looks at the code while running and tries to identify the so-called "hot parts" of that code (parts that are executed more often than others). The JIT will take that source code and compile it on the fly to a more optimized, machine-friendly blob of code, which can be run instead. Interestingly, this is only possible in interpreted languages because programs which are fully compiled beforehand can't change anymore.The mechanism that tries to identify hot parts is called a "monitor": it will look at the code, and monitor it while running. When it detects parts that are executed several times, it will mark them as "warm" or "hot". It can then compile the hot parts into optimized blobs of code. You can imagine there's a lot more complexity to this topic, 

but this book's goal isn't to explain the JIT compiler in depth. Instead, it's to teach you how and when to use it in PHP.

While this might sound great in theory, there are a few sidenotes to be made. First of all: monitoring code and generating JIT'ed code also comes with a performance cost. 

Luckily the benefits gained from the JIT outweigh that cost. At least, in some cases.

The second problem is more important: there aren't many hot parts to optimise in a regular MVC application serving web requests. When the JIT was still in its early days, 

a popular example was shared within the PHP community. It showed a fractal being generated with and without the JIT. The JIT'ed version was significant — tens times 

— faster. But let's be honest: we're very rarely generating fractal images in our PHP applications.

Even on the framework level, there's very little code that benefits from an optimized JIT'ed version. The main performance bottleneck in web applications isn't the code itself; it's I/O operations like sending and receive requests, reading data from the file system, or communicating with a database server.

We're speculating about the JIT's performance at this point. Let's look at some real-life benchmarks instead. I took a Laravel project with its production database and decided to benchmark it.

Real -Life Benchmarks Let's set the scene first. These benchmarks were run on my local machine. Conse -

quently, they don't say anything about absolute performance gains; here, I'm only in -

terested in making conclusions about the relative impact the JIT has on real-life code.

I'll be running PHP FPM, configured to spawn 20 child processes, and I'll always make sure to only run 20 concurrent requests at once, to eliminate any extra performance hits on the FPM level. Sending these requests is done using the following command, 

with ApacheBench:

ab -n 100 -c 20 -l localhost:8000 JIT Setup With the project in place, let's configure the JIT itself. The JIT is enabled by specifying the opcache.jit_buffer_size  option in php.ini . If this directive is excluded, the default value is set to 0, and the JIT won't run.

opcache.jit_buffer_size=100M You'll also want to set a JIT mode, which will determine how the JIT will monitor and react to hot parts of your code. You'll need to use the opcache.jit  option. Its default is set to tracing , but you can set it to function  as well:

opcache.jit=function

; opcache.jit=tracingThe tracing  or function  mode will determine how the JIT will work. The difference is that the function  JIT will only monitor and compile code within the context of a single function, while the tracing  JIT can look across those boundaries. In our real-life benchmarks, I'll compare both modes with each other. So let's start benchmarking!

Establishing a Baseline First, it's best to establish whether the JIT is working properly or not. We know from the RFC that it does have a significant impact on calculating a fractal. So let's start with that example. I copied the mandelbrot example from the RFC and accessed it via the same HTTP application I'll run the next benchmarks on:

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

```

}After running ab for a few hundred requests, we can see the results:

                                      requests/second (more is better)

Mandelbrot without JIT                                            3.60 Mandelbrot with tracing JIT                                      41.36 Great, it looks like the JIT is working! There's even a ten times performance increase!

If you want to verify whether the JIT is running, you can use opcache_get_status() , it has a jit entry which lists all relevant information:

```php
print_r(opcache_get_status()['jit']);

```

// array:7 [

//   "enabled" => true

//   "on" => true

//   "kind" => 5

//   "opt_level" => 4

//   "opt_flags" => 6

//   "buffer_size" => 104857584

//   "buffer_free" => 104478688

// ]

Having verified it works as expected, let's move on to our first real-life comparison. 

We're going to compare running our code without the JIT, with the function JIT, and the tracing JIT, both are using 100MB of memory. The page we're going to benchmark shows an overview of posts, so there's some recursion happening. We're also touching several core parts of Laravel: routing, the dependency container, as well as the ORM layer.

                                      requests/second (more is better)

No JIT                                                           63.56 Function JIT                                                     66.32 Tracing JIT                                                      69.45 Here we see the results: enabling the JIT only has a slight improvement. In fact, 

running the benchmarks repeatedly, the results differ slightly every time: I've even seen cases where a JIT enabled run performs worse than the non JIT'ed version. 

Before drawing conclusions, let's bump the memory buffer limit. We'll give the JIT a little more room to breathe with 500MB of memory instead of 100MB.

                                      requests/second (more is better)

No JIT                                                           71.69 Function JIT                                                     72.82 Tracing JIT                                                      70.11 Here we have a case of the JIT performing worse. Like I said at the beginning of this chapter: I want to measure the relative impact of the JIT on real-life web projects. It's clear from these tests that sometimes there might be benefits, but it's in no way as noticeable as the fractal example we started with. I admit I'm not surprised by that. 

Like I wrote before: there's very little hot code to be optimised in real-life applications. 

We're only rarely doing fractal-like computations.

So am I saying there's no need for the JIT? Not quite. I think the JIT can open up new areas for PHP: areas where complex computations do benefit from JIT'ed code. I'm thinking about machine learning and parsers, stuff like that. The JIT might give the PHP community opportunities that didn't exist yet, but it's unclear to say anything with certainty at this point.For example, there's a package called nikic/php-parser  - a PHP implementation that can take PHP code and parse into structured data. This package is actually used by static analysis tools like Psalm, and it turns out this one does benefit a lot from the JIT. 

So even today, there's already advantages, just not when running a web application.

A Complexity to Maintain Adding the JIT to PHP's core also comes with the added maintenance cost. Because the JIT generates machine code, you can imagine it's complex material for a higher level programmer to understand. Say there is a bug in the JIT compiler. For that, you need a developer who knows how to fix it. In this JIT's case, Dmitry Stogov did most programming on it, and there's only a handful of people who understand how it works.

With just a few people being able to maintain such a codebase today, the question whether the JIT compiler can be maintained properly seems justified. Of course, 

people can learn how the compiler works, but it is a complex matter nevertheless. 

I don't think this should be a reason to ditch the JIT, but the cost of maintenance should still be carefully considered. In the first instance, by the ones maintaining the code and the userland community, who should also be aware that some bugfixes or version updates might take longer than what we're used to right now.

Do You Want It?

If you think that the JIT offers little short-term benefits for your web applications, I'd say you're right. It's clear that its impact will be minimal at best.

Despite that, we should remember that the JIT can open many possibilities for PHP to grow, both as a web language and a more generally purposed language. So the ques -

tion that needs answering: is this possibly a bright future worth the investment today?

Time will tell.
