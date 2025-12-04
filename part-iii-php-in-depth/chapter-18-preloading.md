# CHAPTER 18

## PRELOADING Another core feature focused on performance is preloading, added in PHP 7.4. It's a feature that can improve your code's performance significantly, by loading cached PHP files into memory on server startup. Preloading is done by using a dedicated preload script — which you have to write yourself or generate. The script is executed once on server startup, and all PHP files loaded from within that script will be available in-memory for all following requests. In this chapter, I'll show you how to set up and use preloading and share benchmarks as I did with the JIT.

Let's start by discussing preloading in depth.

Opcache, But More Preloading itself is built on top of opcache, but it's not exactly the same. Opcache will take your PHP source files at runtime, compile them to "opcodes", and store those compiled files on disk. You can think of opcodes as a low-level representation of your code that can be easily interpreted at runtime. The next time a cached file is request -

ed, the translation step can be skipped, and the file can be read from disk. In practice a simple PHP instructions like this one:

echo 1 + 2;Would be translated to opcodes like so:

line     #        op           fetch          ext  return  operands

---------------------------------------------------------------------

   6     0        ADD                              -0      1,2 1        ECHO                                     ~0 7     2        RETURN                                   1 Opcache already speeds up PHP significantly, but there's more to be gained. Most importantly: opcached files don't know about other files. If you've got a class Order extending from a class Model , PHP still needs to link them together at runtime.

So this is where preloading comes into play: it will not only compile source files to opcodes but also link related classes, traits, and interfaces together. It will then keep this "compiled" blob of runnable code — that is: code usable by the PHP interpreter — 

in memory. When a request arrives at the server, it can now use parts of the codebase that were already loaded in memory, without any overhead.

Preloading improves performance even more compared to opcache, since it already links files, doesn't have to read cached opcodes from disk, and doesn't deal with in -

validating cache. Once a file is cached, it's there to stay until the server restarts.

So, which files exactly can be preloaded? And how do you do that?

Preloading in Practice For preloading to work, you — the developer — has to tell the server which files to load. This is done with a simple PHP script, which can include other files. The rules are simple:

• You provide a preload script and link it in your php.ini  file using opcache.preload

• Every PHP file you want to be preloaded should be loaded within that script. You can either use opcache_compile_file()  or require_once  to do so.

Say you want to preload the Laravel framework. Your script will have to loop over all PHP files in the vendor/laravel  directory and include them individually.

Here's how you'd link to this script in php.ini :

opcache.preload=/path/to/project/preload.php And here's a dummy implementation of that preload file:

```php
$files = /* An array of files you want to preload */;

foreach ($files as $file) {

    opcache_compile_file($file);

}

```

Warning: Can't Preload Unlinked Class Hang on; there's a caveat! For files to be preloaded, their dependencies — interfaces, 

traits, and parent classes — must also be preloaded. If there are any problems with the class dependencies, you'll be notified of it on server start up:

Can't preload unlinked class Illuminate\Database\Query\JoinClause:

Unknown parent Illuminate\Database\Query\BuilderThis is the linking part I discussed earlier: the dependencies of preloaded files must also be loaded; otherwise, PHP can't preload them. This isn't a fatal error, by the way 

- your server will start up just fine - but it indicates that not all files you wanted to preload were able to do so.

Luckily, there's a way to ensure all dependencies of a PHP file are loaded as well: 

instead of using opcache_compile_file  you can use require_once , and let the registered autoloader (probably composer's) take care of the rest.

```php
$files = /* All files in eg. vendor/laravel */;

foreach ($files as $file) {

    require_once($file);

}

```

There are still some caveats. If you're trying to preload Laravel, for example, some classes within the framework have dependencies on other classes that don't exist yet. 

For example, the filesystem cache class \Illuminate\Filesystem\Cache  has a depen -

dency on \League\Flysystem\Cached\Storage\AbstractCache , which might not be installed in your project if you're never using filesystem caches.

You might run into "class not found" errors trying to preload everything. And the only solution is to skip those files from preloading. Luckily in a default Laravel installation, 

there's only a handful of these classes, which can easily be ignored. For convenience, 

I wrote a little preloader class to make ignoring files easier, and here's what it looks like:

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

By adding this class in the same preload script, we're now able to load the whole Laravel framework like so:

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

So keep in mind that every time you make a change to the preload script, or any of its preloaded files, you'll have to restart the server. I don't mean physically rebooting the whole server, though; restarting php-fpm  is enough. If you're on a Linux machine it's as easy as running sudo service php8.0-fpm restart . Replace 8.0 with the version you are on.

Does It Work?

With all those preloaded files, are we sure they were correctly loaded? You can simply test it by restarting the server, and dumping the output of opcache_get_status()  in a PHP script. You'll see a key called preload_statistics , which will list all preloaded functions, classes, and scripts, as well as the memory consumed by the preloaded files.

There's one more important thing to mention about the operations side when using preloading. You already know that you need to specify an entry in php.ini  for preloading to work. If you're using shared hosting, you won't be able to freely configure PHP whatever way you want. In practice, you'll need a dedicated (virtual) server to be able to optimise the preloaded files for a single project. So keep that in mind.

On to the most important question: does preloading improve performance? Well, let's benchmark it! Like with the JIT, I'll do a practical benchmark measuring relative results and measure a real-life project. It's important to know whether preloading is worth your time in your own projects, and not just in a theoretical benchmark. This project is the same Laravel project as in the previous chapter: it will again do some database calls, view rendering, etc.

Let's set the stage.

Preloading Setup Since I'm mostly interested in the relative impact preloading has on my code, I decided to run these benchmarks on my local machine using Apache Bench. I'll be sending 5000 requests, with 50 concurrent requests at a time. The webserver is Nginx, using PHP-FPM. Because there were some bugs in early versions of preloading, I'm only able to successfully run these benchmarks as early as PHP 7.4.2.

I'll be benchmarking three scenarios: one with preloading disabled, one with all Laravel and application code preloaded, and one with an optimised list of preloaded classes. 

The reasoning for that latter one is that preloading also comes with a memory over -

head. If we're only preloading "hot" classes — classes that are used very often — we might be able to find a sweet spot between performance gain and memory usage.

Preloading Disabled We start php-fpm without preloading enabled and run our benchmarks:

./php-7_4_2/sbin/php-fpm =-nodaemonize ab -n 5000 -c 50 -l localhost:8000 These were the results: we're able to process 64.79 requests per second, with an average time of 771ms per request. This is our baseline scenario, where we can compare the next results to this one.Naive Preloading Next, we'll preload all Laravel and application code. This is the naive approach because we're never using all Laravel classes in a request. We're preloading many more files than strictly needed, so we'll have to pay a penalty for it. In this case, 1165 files and their dependencies were preloaded, resulting in 1366 functions and 1256 classes to be included.

Like I mentioned before, you can read that info from opcache_get_status() :

```php
opcache_get_status()['preload_statistics'];

```

Another metric we get from opcache_get_status()  is the memory used for preloaded scripts. In this case it's 17.43 MB. Even though we're preloading more code than we actually need, naive preloading already has a positive impact on performance.

                           requests/second            time per request No preloading                        64.79                       771ms Naive preloading                     79.69                       627ms You can already see a performance gain: we can manage more requests per second, 

and the average amount of time to process one request has dropped by ±20%.

Optimised Finally, we want to compare the performance gain when we're using an optimised preloading list. For testing purposes, I started the server without preloading enabled and dumped all classes that are used within that request:

```php
get_declared_classes();

```

Next, I only preloaded these classes (427 in total). Together with all their depen -

dencies, this makes for 643 classes and 1034 functions being preloaded, occupying about 11.76 MB of memory.

These are the benchmark results for this setup:

                           requests/second            time per request No preloading              64.79                                 771ms Naive preloading           79.69                                 627ms Optimised preloading       86.12                                 580ms That's around a 25% performance gain compared to not using preloading and an 8% 

gain compared to using the naive approach. There's a flaw with this setup though, 

since I generated an optimised preloading list for one specific page. In practice, you would probably need to preload more code, if you want all your pages covered.

Another approach could be to monitor which classes are loaded how many times over several hours or days on your production server and compile a preload list based on those metrics. A package that does this is called darkghosthunter/preloader . It's definitely worth checking out.

It's safe to say that preloading — even using the naive "preload everything" approach 

— has a positive performance impact, also on real-life projects built upon a full-blownframework. However, there's still an important side note to be made. Real-life applica -

tions will most likely not experience a 25% increase in performance. That is because they do many more things than just booting a framework. An important thing I can think about is I/O: communicating with a database server, reading and writing to the filesystem, integrating with third party services, etc. So while preloading can optimise the booting part of your code, there still might be other areas that have a much larger impact on performance. How much exactly there is to be gained will depend on your code, server, and framework you're using. I'd say go try it out, and don't forget to measure the results.
