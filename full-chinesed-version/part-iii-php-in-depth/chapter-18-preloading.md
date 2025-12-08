# 第十八章

## 预加载

另一个专注于性能的核心功能是预加载，在 PHP 7.4 中添加。这是一个可以通过在服务器启动时将缓存的 PHP 文件加载到内存中来显著提高代码性能的功能。预加载是通过使用专用的预加载脚本完成的——你必须自己编写或生成。脚本在服务器启动时执行一次，从该脚本中加载的所有 PHP 文件将在内存中可用于所有后续请求。在本章中，我将向你展示如何设置和使用预加载，并像我对 JIT 所做的那样分享基准测试。

让我们开始深入讨论预加载。

## Opcache，但更多

预加载本身建立在 opcache 之上，但它并不完全相同。Opcache 将在运行时获取你的 PHP 源文件，将它们编译为"操作码"，并将这些编译的文件存储在磁盘上。你可以将操作码视为代码的低级表示，可以在运行时轻松解释。下次请求缓存文件时，

可以跳过翻译步骤，可以从磁盘读取文件。在实践中，像这样的简单 PHP 指令：

echo 1 + 2;将被翻译为操作码，如下所示：

line     #        op           fetch          ext  return  operands

---------------------------------------------------------------------

   6     0        ADD                              -0      1,2 1        ECHO                                     ~0 7     2        RETURN                                   1 Opcache 已经显著加快了 PHP 的速度，但还有更多可以获得的。最重要的是：opcached 文件不知道其他文件。如果你有一个类 Order 从类 Model 扩展，PHP 仍然需要在运行时将它们链接在一起。

所以这就是预加载发挥作用的地方：它不仅会将源文件编译为操作码，还会将相关的类、trait 和接口链接在一起。然后它将保留这个"编译的"可运行代码块——即：PHP 解释器可用的代码——

在内存中。当请求到达服务器时，它现在可以使用已经加载到内存中的代码库部分，而没有任何开销。

与 opcache 相比，预加载进一步提高了性能，因为它已经链接文件，不必从磁盘读取缓存的操作码，并且不处理无效

缓存。一旦文件被缓存，它就会一直存在，直到服务器重启。

那么，到底哪些文件可以被预加载？你如何做到这一点？

## 实践中的预加载

为了使预加载工作，你——开发人员——必须告诉服务器要加载哪些文件。这是通过一个简单的 PHP 脚本完成的，它可以包含其他文件。规则很简单：

• 你提供一个预加载脚本，并使用 opcache.preload 在 php.ini 文件中链接它

• 你想要预加载的每个 PHP 文件都应该在该脚本中加载。你可以使用 opcache_compile_file() 或 require_once 来这样做。

假设你想预加载 Laravel 框架。你的脚本必须循环遍历 vendor/laravel 目录中的所有 PHP 文件并单独包含它们。

以下是你如何在 php.ini 中链接到此脚本：

opcache.preload=/path/to/project/preload.php 以下是该预加载文件的虚拟实现：

```php
$files = /* An array of files you want to preload */;

foreach ($files as $file) {

    opcache_compile_file($file);

}

```

## 警告：无法预加载未链接的类

等等；有一个警告！对于要预加载的文件，它们的依赖项——接口、

trait 和父类——也必须被预加载。如果类依赖项有任何问题，你将在服务器启动时收到通知：

Can't preload unlinked class Illuminate\Database\Query\JoinClause:

Unknown parent Illuminate\Database\Query\Builder

这是我之前讨论的链接部分：预加载文件的依赖项也必须被加载；否则，PHP 无法预加载它们。顺便说一下，这不是致命错误

——你的服务器将正常启动——但它表明并非所有你想要预加载的文件都能够这样做。

幸运的是，有一种方法可以确保 PHP 文件的所有依赖项也被加载：

你可以使用 require_once 而不是使用 opcache_compile_file，并让注册的自动加载器（可能是 composer 的）处理其余部分。

```php
$files = /* All files in eg. vendor/laravel */;

foreach ($files as $file) {

    require_once($file);

}

```

仍然有一些警告。例如，如果你试图预加载 Laravel，框架中的某些类依赖于尚不存在的其他类。

例如，文件系统缓存类 \Illuminate\Filesystem\Cache 依赖于

\League\Flysystem\Cached\Storage\AbstractCache，如果你从不使用文件系统缓存，它可能不会安装在你的项目中。

你可能在尝试预加载所有内容时遇到"类未找到"错误。唯一的解决方案是从预加载中跳过这些文件。幸运的是，在默认的 Laravel 安装中，

只有少数这些类，可以轻松忽略。为了方便，

我编写了一个小的预加载器类，使忽略文件更容易，以下是它的样子：

```php
class Preloader

{

    private array $ignores = [];

    private static int $count = 0;

    private array $paths;

    private array $fileMap;

    public function =_construct(string ==.$paths)

    {
$this=>paths = $paths;

```

        // We'll use composer's classmap
        // to easily find which classes to autoload,
        // based on their filename

```php
$classMap = require =_DIR=_ . 

            '/vendor/composer/autoload_classmap.php';

```

        // We flip the array, so that file paths are the array keys
        // With it, we can search the corresponding class by its path

```php
$this=>fileMap = array_flip($classMap);

```

    }public function paths(string ==.$paths): Preloader

```php
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

```

        // We'll loop over all registered paths

```php
        // and load them one by one foreach ($this=>paths as $path) {
$this=>loadPath(rtrim($path, '/'));

        }
$count = self=:$count;

        echo "[Preloader] Preloaded {$count} classes" . PHP_EOL;

    }

    private function loadPath(string $path): void

    {

```

        // If the current path is a directory,

```php
        // we'll load all files in it if (is_dir($path)) {
$this=>loadDir($path);

            return;

        }

```

        // Otherwise we'll just load this one file

```php
$this=>loadFile($path);

```

    }private function loadDir(string $path): void

```php
    {
$handle = opendir($path);

```

        // We'll loop over all files and directories
        // in the current path,

```php
        // and load them one by one while ($file = readdir($handle)) {

            if (in_array($file, ['.', '=.'])) {

                continue;

            }
$this=>loadPath("{$path}/{$file}");

        }

        closedir($handle);

    }

    private function loadFile(string $path): void

    {

```

        // We resolve the classname from composer's autoload mapping

```php
$class = $this=>fileMap[$path] =? null;

        // And use it to make sure the class shouldn't be ignored if ($this=>shouldIgnore($class)) {

            return;

        }

```

        // Finally we require the path,

```php
        // causing all its dependencies to be loaded as well require_once($path);

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

```

通过在同一预加载脚本中添加此类，我们现在能够像这样加载整个 Laravel 框架：

// …

(new Preloader())

    =>paths(=_DIR=_ . '/vendor/laravel')

    =>ignore(

        \Illuminate\Filesystem\Cache=:class,

        \Illuminate\Log\LogManager=:class,

        \Illuminate\Http\Testing\File=:class,\Illuminate\Http\UploadedFile=:class,

        \Illuminate\Support\Carbon=:class,

    )

```php
    =>load();

```

所以请记住，每次你对预加载脚本或其任何预加载文件进行更改时，都必须重启服务器。不过，我不是指物理重启整个服务器；重启 php-fpm 就足够了。如果你在 Linux 机器上，就像运行 sudo service php8.0-fpm restart 一样简单。将 8.0 替换为你使用的版本。

## 它有效吗？

有了所有这些预加载的文件，我们确定它们被正确加载了吗？你可以简单地通过重启服务器并在 PHP 脚本中转储 opcache_get_status() 的输出来测试它。你将看到一个名为 preload_statistics 的键，它将列出所有预加载的函数、类和脚本，以及预加载文件消耗的内存。

关于使用预加载时的操作方面，还有一件重要的事情要提及。你已经知道你需要为预加载在 php.ini 中指定一个条目。如果你使用共享主机，你将无法自由配置 PHP 的任何方式。在实践中，你需要一个专用的（虚拟）服务器，以便能够为单个项目优化预加载的文件。所以请记住这一点。

关于最重要的问题：预加载是否提高了性能？嗯，让我们对其进行基准测试！就像 JIT 一样，我将进行一个实际基准测试，测量相对结果并测量实际项目。重要的是要知道预加载是否值得你在自己的项目中花费时间，而不仅仅是在理论基准测试中。这个项目与前一章中的 Laravel 项目相同：它将再次进行一些数据库调用、视图渲染等。

让我们设置场景。

## 预加载设置

由于我主要对预加载对我的代码的相对影响感兴趣，我决定使用 Apache Bench 在我的本地机器上运行这些基准测试。我将发送 5000 个请求，一次 50 个并发请求。Web 服务器是 Nginx，使用 PHP-FPM。因为早期版本的预加载存在一些 bug，我只能从 PHP 7.4.2 开始成功运行这些基准测试。

我将对三种场景进行基准测试：一种禁用预加载，一种预加载所有 Laravel 和应用程序代码，一种使用优化的预加载类列表。

后者的原因是预加载也带来了内存开销。

如果我们只预加载"热点"类——使用非常频繁的类——我们可能能够在性能提升和内存使用之间找到一个最佳点。

## 禁用预加载

我们在没有启用预加载的情况下启动 php-fpm 并运行我们的基准测试：

./php-7_4_2/sbin/php-fpm =-nodaemonize ab -n 5000 -c 50 -l localhost:8000 这些是结果：我们能够每秒处理 64.79 个请求，每个请求的平均时间为 771ms。这是我们的基线场景，我们可以将下一个结果与此进行比较。

## 简单预加载

接下来，我们将预加载所有 Laravel 和应用程序代码。这是简单的方法，因为我们在一个请求中从不使用所有 Laravel 类。我们预加载的文件比严格需要的多得多，所以我们必须为此付出代价。在这种情况下，预加载了 1165 个文件及其依赖项，导致包含 1366 个函数和 1256 个类。

就像我之前提到的，你可以从 opcache_get_status() 中读取该信息：

```php
opcache_get_status()['preload_statistics'];

```

我们从 opcache_get_status() 获得的另一个指标是用于预加载脚本的内存。在这种情况下，它是 17.43 MB。即使我们预加载的代码比实际需要的多，简单预加载已经对性能产生了积极影响。

                           requests/second            time per request No preloading                        64.79                       771ms Naive preloading                     79.69                       627ms 你已经可以看到性能提升：我们可以每秒管理更多请求，

处理一个请求的平均时间下降了约 20%。

## 优化

最后，我们想比较使用优化的预加载列表时的性能提升。为了测试目的，我在没有启用预加载的情况下启动服务器，并转储了在该请求中使用的所有类：

```php
get_declared_classes();

```

接下来，我只预加载了这些类（总共 427 个）。与它们的所有依赖项一起，

这使得预加载了 643 个类和 1034 个函数，占用约 11.76 MB 的内存。

这是此设置的基准测试结果：

                           requests/second            time per request No preloading              64.79                                 771ms Naive preloading           79.69                                 627ms Optimised preloading       86.12                                 580ms 与不使用预加载相比，性能提升约 25%，与使用简单方法相比，性能提升 8%。

不过，这个设置有一个缺陷，

因为我为一个特定页面生成了优化的预加载列表。在实践中，如果你想覆盖所有页面，你可能需要预加载更多代码。

另一种方法可能是监控在生产服务器上几个小时或几天内加载了多少次哪些类，并基于这些指标编译预加载列表。一个这样做的包称为 darkghosthunter/preloader。绝对值得查看。

可以安全地说，预加载——即使使用简单的"预加载所有内容"方法

——对性能有积极影响，也适用于基于完整框架构建的实际项目。但是，仍然有一个重要的注意事项。实际应用程序

很可能不会经历 25% 的性能提升。那是因为它们做的事情比启动框架多得多。我能想到的一件重要事情是 I/O：与数据库服务器通信、读取和写入文件系统、与第三方服务集成等。所以虽然预加载可以优化代码的启动部分，但可能还有其他领域对性能有更大的影响。确切地说，有多少可以获得的将取决于你的代码、服务器和你使用的框架。我会说去试试，不要忘记测量结果。

