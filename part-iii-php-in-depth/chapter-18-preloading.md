# Chapter 18: Preloading

Another core feature focused on performance is preloading, added in PHP 7.4. It's a

另一个专注于性能的核心功能是预加载，在 PHP 7.4 中添加。这是一个可以通过在服务器启动时将缓存的 PHP 文件加载到内存中来显著提高代码性能的功能。预加载通过使用专用的预加载脚本完成——你必须自己编写或生成。脚本在服务器启动时执行一次，从该脚本中加载的所有 PHP 文件将在内存中可用于所有后续请求。在本章中，我将向你展示如何设置和使用预加载，并像我对 JIT 那样分享基准测试。

feature that can improve your code's performance significantly, by loading cached

让我们开始深入讨论预加载。

PHP files into memory on server startup. Preloading is done by using a dedicated

预加载本身建立在 opcache 之上，但它并不完全相同。Opcache 将在运行时获取你的 PHP 源文件，将它们编译为"opcodes"（操作码），并将这些编译的文件存储在磁盘上。你可以将 opcodes 视为代码的低级表示，可以在运行时轻松解释。下次请求缓存文件时，可以跳过翻译步骤，可以从磁盘读取文件。实际上，像这样的简单 PHP 指令：

preload script — which you have to write yourself or generate. The script is executed

将被翻译为如下 opcodes：

once on server startup, and all PHP files loaded from within that script will be available

Opcache 已经显著加快了 PHP 的速度，但还有更多可以获得的。最重要的是：opcached 文件不知道其他文件。如果你有一个 `Order` 类从 `Model` 类扩展，PHP 仍然需要在运行时将它们链接在一起。

in-memory for all following requests. In this chapter, I'll show you how to set up and

所以这就是预加载发挥作用的地方：它不仅会将源文件编译为 opcodes，还会将相关的类、trait 和接口链接在一起。然后它将把这个"编译的"可运行代码块——即：PHP 解释器可用的代码——保存在内存中。当请求到达服务器时，它现在可以使用已经加载到内存中的代码库部分，而没有任何开销。

use preloading and share benchmarks as I did with the JIT.

与 opcache 相比，预加载进一步提高了性能，因为它已经链接了文件，不必从磁盘读取缓存的 opcodes，并且不处理缓存失效。一旦文件被缓存，它就会一直存在，直到服务器重启。

Let's start by discussing preloading in depth.

那么，到底哪些文件可以被预加载？你如何做到这一点？

Opcache, But More

为了使预加载工作，你——开发者——必须告诉服务器要加载哪些文件。这是通过一个简单的 PHP 脚本完成的，该脚本可以包含其他文件。规则很简单：

Preloading itself is built on top of opcache, but it's not exactly the same. Opcache will

- 你提供一个预加载脚本，并在 `php.ini` 文件中使用 `opcache.preload` 链接它
- 你想要预加载的每个 PHP 文件都应该在该脚本中加载。你可以使用 `opcache_compile_file()` 或 `require_once` 来这样做。

take your PHP source files at runtime, compile them to "opcodes", and store those

假设你想预加载 Laravel 框架。你的脚本必须循环遍历 `vendor/laravel` 目录中的所有 PHP 文件并单独包含它们。

compiled files on disk. You can think of opcodes as a low-level representation of your

以下是你如何在 `php.ini` 中链接到此脚本：

code that can be easily interpreted at runtime. The next time a cached file is request-

这是该预加载文件的虚拟实现：

ed, the translation step can be skipped, and the file can be read from disk. In practice

**警告：无法预加载未链接的类**

a simple PHP instructions like this one:

等等；有一个注意事项！要预加载文件，它们的依赖——接口、trait 和父类——也必须被预加载。如果类依赖有任何问题，你将在服务器启动时收到通知：

echo 1 + 2;

这是我之前讨论的链接部分：预加载文件的依赖也必须被加载；否则，PHP 无法预加载它们。顺便说一下，这不是致命错误——你的服务器会正常启动——但它表明并非所有你想要预加载的文件都能这样做。

202

幸运的是，有一种方法可以确保 PHP 文件的所有依赖也被加载：你可以使用 `require_once` 而不是 `opcache_compile_file`，让注册的自动加载器（可能是 composer 的）处理其余部分。

Would be translated to opcodes like so:

仍然有一些注意事项。例如，如果你尝试预加载 Laravel，框架内的一些类依赖于其他还不存在的类。例如，文件系统缓存类 `\Illuminate\Filesystem\Cache` 依赖于 `\League\Flysystem\Cached\Storage\AbstractCache`，如果你从不使用文件系统缓存，它可能不会安装在你的项目中。

line     #        op           fetch          ext  return  operands

你可能在尝试预加载所有内容时遇到"类未找到"错误。唯一的解决方案是从预加载中跳过那些文件。幸运的是，在默认的 Laravel 安装中，只有少数这样的类，可以轻松忽略。为了方便，我编写了一个小的预加载器类，使忽略文件更容易，这是它的样子：

---------------------------------------------------------------------

通过在同一预加载脚本中添加此类，我们现在可以像这样加载整个 Laravel 框架：

6     0        ADD                              -0      1,2

所以请记住，每次你对预加载脚本或其任何预加载文件进行更改时，你都必须重启服务器。我的意思不是物理重启整个服务器；重启 php-fpm 就足够了。如果你在 Linux 机器上，就像运行 `sudo service php8.0-fpm restart` 一样简单。将 8.0 替换为你使用的版本。

1        ECHO                                     ~0

有了所有这些预加载的文件，我们确定它们被正确加载了吗？你可以简单地通过重启服务器并在 PHP 脚本中转储 `opcache_get_status()` 的输出来测试它。你会看到一个名为 `preload_statistics` 的键，它将列出所有预加载的函数、类和脚本，以及预加载文件消耗的内存。

7     2        RETURN                                   1

关于使用预加载时的操作方面，还有一件重要的事情要提到。你已经知道需要为预加载在 `php.ini` 中指定一个条目。如果你使用共享主机，你将无法自由配置 PHP。实际上，你需要一个专用（虚拟）服务器才能为单个项目优化预加载文件。所以请记住这一点。

Opcache already speeds up PHP significantly, but there's more to be gained. Most

最重要的是：预加载是否提高了性能？让我们进行基准测试！就像 JIT 一样，我将做一个实用的基准测试，测量相对结果并测量一个现实项目。重要的是要知道预加载是否值得你在自己的项目中花费时间，而不仅仅是在理论基准测试中。这个项目与前一章中的 Laravel 项目相同：它还会进行一些数据库调用、视图渲染等。

importantly: opcached files don't know about other files. If you've got a class Order

让我们设置场景。

extending from a class Model, PHP still needs to link them together at runtime.

由于我主要对预加载对我的代码的相对影响感兴趣，我决定使用 Apache Bench 在本地机器上运行这些基准测试。我将发送 5000 个请求，每次 50 个并发请求。Web 服务器是 Nginx，使用 PHP-FPM。因为早期版本的预加载存在一些错误，我只能从 PHP 7.4.2 开始成功运行这些基准测试。

So this is where preloading comes into play: it will not only compile source files to

我将对三种场景进行基准测试：一种是禁用预加载，一种是预加载所有 Laravel 和应用程序代码，一种是优化预加载类列表。后者的原因是预加载也带来了内存开销。如果我们只预加载"热点"类——经常使用的类——我们可能能够在性能增益和内存使用之间找到一个平衡点。

opcodes but also link related classes, traits, and interfaces together. It will then keep

我们在没有启用预加载的情况下启动 php-fpm 并运行我们的基准测试：

this "compiled" blob of runnable code — that is: code usable by the PHP interpreter —

这些是结果：我们能够每秒处理 64.79 个请求，每个请求的平均时间为 771ms。这是我们的基线场景，我们可以将下一个结果与此进行比较。

in memory. When a request arrives at the server, it can now use parts of the codebase

接下来，我们将预加载所有 Laravel 和应用程序代码。这是简单的方法，因为我们永远不会在请求中使用所有 Laravel 类。我们预加载的文件比严格需要的多得多，所以我们必须为此付出代价。在这种情况下，预加载了 1165 个文件及其依赖，导致包含 1366 个函数和 1256 个类。

that were already loaded in memory, without any overhead.

就像我之前提到的，你可以从 `opcache_get_status()` 中读取该信息：

Preloading improves performance even more compared to opcache, since it already

我们从 `opcache_get_status()` 得到的另一个指标是用于预加载脚本的内存。在这种情况下是 17.43 MB。即使我们预加载的代码比我们实际需要的多，简单预加载已经对性能产生了积极影响。

links files, doesn't have to read cached opcodes from disk, and doesn't deal with in-

你已经可以看到性能提升：我们可以每秒处理更多请求，处理一个请求的平均时间下降了约 20%。

validating cache. Once a file is cached, it's there to stay until the server restarts.

最后，我们想比较使用优化的预加载列表时的性能提升。为了测试目的，我在没有启用预加载的情况下启动了服务器，并转储了在该请求中使用的所有类：

So, which files exactly can be preloaded? And how do you do that?

接下来，我只预加载这些类（总共 427 个）。连同它们的所有依赖，这使 643 个类和 1034 个函数被预加载，占用约 11.76 MB 的内存。

Preloading in Practice

这是此设置的基准测试结果：

For preloading to work, you — the developer — has to tell the server which files to

与不使用预加载相比，性能提升约 25%，与使用简单方法相比，性能提升约 8%。不过，这个设置有一个缺陷，因为我为特定页面生成了优化的预加载列表。实际上，如果你想覆盖所有页面，你可能需要预加载更多代码。

load. This is done with a simple PHP script, which can include other files. The rules are

另一种方法可能是监控在你的生产服务器上几个小时或几天内加载了哪些类以及加载了多少次，并根据这些指标编译预加载列表。一个这样做的包叫做 `darkghosthunter/preloader`。绝对值得一试。

simple:

可以安全地说，预加载——即使使用简单的"预加载一切"方法——也有积极的性能影响，即使在基于完整框架的现实项目上也是如此。然而，仍然有一个重要的注意事项。现实应用程序很可能不会体验到 25% 的性能提升。那是因为它们做的事情比仅仅启动框架多得多。我能想到的一件重要事情是 I/O：与数据库服务器通信、读写文件系统、与第三方服务集成等。所以虽然预加载可以优化代码的启动部分，但可能还有其他领域对性能有更大的影响。确切能获得多少收益将取决于你的代码、服务器和使用的框架。我会说去试试，不要忘记测量结果。

Chapter 18 - Preloading

•  You provide a preload script and link it in your php.ini file using

opcache.preload

•  Every PHP file you want to be preloaded should be loaded within that script. You

can either use opcache_compile_file() or require_once to do so.

Say you want to preload the Laravel framework. Your script will have to loop over all

PHP files in the vendor/laravel directory and include them individually.

Here's how you'd link to this script in php.ini:

opcache.preload=/path/to/project/preload.php

And here's a dummy implementation of that preload file:

$files = /* An array of files you want to preload */;

foreach ($files as $file) {

opcache_compile_file($file);

}

Warning: Can't Preload Unlinked Class

Hang on; there's a caveat! For files to be preloaded, their dependencies — interfaces,

traits, and parent classes — must also be preloaded. If there are any problems with

the class dependencies, you'll be notified of it on server start up:

Can't preload unlinked class Illuminate\Database\Query\JoinClause:

Unknown parent Illuminate\Database\Query\Builder

204

This is the linking part I discussed earlier: the dependencies of preloaded files must

also be loaded; otherwise, PHP can't preload them. This isn't a fatal error, by the way

- your server will start up just fine - but it indicates that not all files you wanted to

preload were able to do so.

Luckily, there's a way to ensure all dependencies of a PHP file are loaded as well:

instead of using opcache_compile_file you can use require_once, and let the regis-

tered autoloader (probably composer's) take care of the rest.

$files = /* All files in eg. vendor/laravel */;

foreach ($files as $file) {

require_once($file);

}

There are still some caveats. If you're trying to preload Laravel, for example, some

classes within the framework have dependencies on other classes that don't exist yet.

For example, the filesystem cache class \Illuminate\Filesystem\Cache has a depen-

dency on \League\Flysystem\Cached\Storage\AbstractCache, which might not be

installed in your project if you're never using filesystem caches.

You might run into "class not found" errors trying to preload everything. And the only

solution is to skip those files from preloading. Luckily in a default Laravel installation,

there's only a handful of these classes, which can easily be ignored. For convenience,

Chapter 18 - Preloading

I wrote a little preloader class to make ignoring files easier, and here's what it looks

like:

class Preloader

{

private array $ignores = [];

private static int $count = 0;

private array $paths;

private array $fileMap;

public function =_construct(string ==.$paths)

{

$this=>paths = $paths;

// We'll use composer's classmap

// to easily find which classes to autoload,

// based on their filename

$classMap = require =_DIR=_ .

'/vendor/composer/autoload_classmap.php';

// We flip the array, so that file paths are the array keys

// With it, we can search the corresponding class by its path

$this=>fileMap = array_flip($classMap);

}

206

public function paths(string ==.$paths): Preloader

{

$this=>paths = array_merge(

$this=>paths,

$paths

);

return $this;

}

public function ignore(string ==.$names): Preloader

{

$this=>ignores = array_merge(

$this=>ignores,

$names

);

return $this;

}

public function load(): void

{

// We'll loop over all registered paths

// and load them one by one

foreach ($this=>paths as $path) {

$this=>loadPath(rtrim($path, '/'));

}

$count = self=:$count;

echo "[Preloader] Preloaded {$count} classes" . PHP_EOL;

}

Chapter 18 - Preloading

private function loadPath(string $path): void

{

// If the current path is a directory,

// we'll load all files in it

if (is_dir($path)) {

$this=>loadDir($path);

return;

}

// Otherwise we'll just load this one file

$this=>loadFile($path);

}

208

private function loadDir(string $path): void

{

$handle = opendir($path);

// We'll loop over all files and directories

// in the current path,

// and load them one by one

while ($file = readdir($handle)) {

if (in_array($file, ['.', '=.'])) {

continue;

}

$this=>loadPath("{$path}/{$file}");

}

closedir($handle);

}

private function loadFile(string $path): void

{

// We resolve the classname from composer's autoload mapping

$class = $this=>fileMap[$path] =? null;

// And use it to make sure the class shouldn't be ignored

if ($this=>shouldIgnore($class)) {

return;

}

// Finally we require the path,

// causing all its dependencies to be loaded as well

require_once($path);

Chapter 18 - Preloading

self=:$count=+;

echo "[Preloader] Preloaded `{$class}`" . PHP_EOL;

}

private function shouldIgnore(?string $name): bool

{

if ($name === null) {

return true;

}

foreach ($this=>ignores as $ignore) {

if (strpos($name, $ignore) === 0) {

return true;

}

}

return false;

}

}

By adding this class in the same preload script, we're now able to load the whole

Laravel framework like so:

// …

(new Preloader())

=>paths(=_DIR=_ . '/vendor/laravel')

=>ignore(

\Illuminate\Filesystem\Cache=:class,

\Illuminate\Log\LogManager=:class,

\Illuminate\Http\Testing\File=:class,

210

\Illuminate\Http\UploadedFile=:class,

\Illuminate\Support\Carbon=:class,

)

=>load();

So keep in mind that every time you make a change to the preload script, or any of its

preloaded files, you'll have to restart the server. I don't mean physically rebooting the

whole server, though; restarting php-fpm is enough. If you're on a Linux machine it's as

easy as running sudo service php8.0-fpm restart. Replace 8.0 with the version you

are on.

Does It Work?

With all those preloaded files, are we sure they were correctly loaded? You can simply

test it by restarting the server, and dumping the output of opcache_get_status() in

a PHP script. You'll see a key called preload_statistics, which will list all preloaded

functions, classes, and scripts, as well as the memory consumed by the preloaded

files.

There's one more important thing to mention about the operations side when using

preloading. You already know that you need to specify an entry in php.ini for pre-

loading to work. If you're using shared hosting, you won't be able to freely configure

PHP whatever way you want. In practice, you'll need a dedicated (virtual) server to be

able to optimise the preloaded files for a single project. So keep that in mind.

On to the most important question: does preloading improve performance? Well, let's

benchmark it! Like with the JIT, I'll do a practical benchmark measuring relative results

and measure a real-life project. It's important to know whether preloading is worth

your time in your own projects, and not just in a theoretical benchmark. This project

is the same Laravel project as in the previous chapter: it will again do some database

calls, view rendering, etc.

Chapter 18 - Preloading

Let's set the stage.

Preloading Setup

Since I'm mostly interested in the relative impact preloading has on my code, I decided

to run these benchmarks on my local machine using Apache Bench. I'll be sending

5000 requests, with 50 concurrent requests at a time. The webserver is Nginx, using

PHP-FPM. Because there were some bugs in early versions of preloading, I'm only

able to successfully run these benchmarks as early as PHP 7.4.2.

I'll be benchmarking three scenarios: one with preloading disabled, one with all Laravel

and application code preloaded, and one with an optimised list of preloaded classes.

The reasoning for that latter one is that preloading also comes with a memory over-

head. If we're only preloading "hot" classes — classes that are used very often — we

might be able to find a sweet spot between performance gain and memory usage.

Preloading Disabled

We start php-fpm without preloading enabled and run our benchmarks:

./php-7_4_2/sbin/php-fpm =-nodaemonize

ab -n 5000 -c 50 -l localhost:8000

These were the results: we're able to process 64.79 requests per second, with an

average time of 771ms per request. This is our baseline scenario, where we can

compare the next results to this one.

212

Naive Preloading

Next, we'll preload all Laravel and application code. This is the naive approach

because we're never using all Laravel classes in a request. We're preloading many

more files than strictly needed, so we'll have to pay a penalty for it. In this case, 1165

files and their dependencies were preloaded, resulting in 1366 functions and 1256

classes to be included.

Like I mentioned before, you can read that info from opcache_get_status():

opcache_get_status()['preload_statistics'];

Another metric we get from opcache_get_status() is the memory used for preloaded

scripts. In this case it's 17.43 MB. Even though we're preloading more code than we

actually need, naive preloading already has a positive impact on performance.

requests/second            time per request

No preloading                        64.79                       771ms

Naive preloading                     79.69                       627ms

You can already see a performance gain: we can manage more requests per second,

and the average amount of time to process one request has dropped by ±20%.

Chapter 18 - Preloading

Optimised

Finally, we want to compare the performance gain when we're using an optimised pre-

loading list. For testing purposes, I started the server without preloading enabled and

dumped all classes that are used within that request:

get_declared_classes();

Next, I only preloaded these classes (427 in total). Together with all their depen-

dencies, this makes for 643 classes and 1034 functions being preloaded, occupying

about 11.76 MB of memory.

These are the benchmark results for this setup:

requests/second            time per request

No preloading              64.79                                 771ms

Naive preloading           79.69                                 627ms

Optimised preloading       86.12                                 580ms

That's around a 25% performance gain compared to not using preloading and an 8%

gain compared to using the naive approach. There's a flaw with this setup though,

since I generated an optimised preloading list for one specific page. In practice, you

would probably need to preload more code, if you want all your pages covered.

Another approach could be to monitor which classes are loaded how many times over

several hours or days on your production server and compile a preload list based on

those metrics. A package that does this is called darkghosthunter/preloader. It's

definitely worth checking out.

It's safe to say that preloading — even using the naive "preload everything" approach

— has a positive performance impact, also on real-life projects built upon a full-blown

214

framework. However, there's still an important side note to be made. Real-life applica-

tions will most likely not experience a 25% increase in performance. That is because

they do many more things than just booting a framework. An important thing I can

think about is I/O: communicating with a database server, reading and writing to the

filesystem, integrating with third party services, etc. So while preloading can optimise

the booting part of your code, there still might be other areas that have a much larger

impact on performance. How much exactly there is to be gained will depend on your

code, server, and framework you're using. I'd say go try it out, and don't forget to

measure the results.

