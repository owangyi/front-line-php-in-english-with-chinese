# CHAPTER 02

## NEW VERSIONS

Since this book aims to bring you up to speed with modern PHP practices, it's important to know what happened to the language over the past decade or so. With the development and release of PHP 7, the PHP landscape changed dramatically. I like to think of the PHP 7.x versions as a maturity phase for the language, so this is where we will start.

由于本书旨在让你快速了解现代 PHP 实践，了解这门语言在过去十年左右发生了什么变化是很重要的。随着 PHP 7 的开发和发布，PHP 的格局发生了巨大变化。我喜欢将 PHP 7.x 版本视为这门语言的成熟阶段，所以我们将从这里开始。

First and foremost, PHP 7.0 comes with a significant performance boost. Much of PHP's core was rewritten, which resulted in a noticeable difference. It's not uncommon to see your application run two or three times as fast, just by using PHP 7 or higher.

首先，PHP 7.0 带来了显著的性能提升。PHP 大部分的核心被重写，这产生了明显的差异。仅仅通过使用 PHP 7 或更高版本，看到你的应用程序运行速度提高两到三倍并不罕见。 

Thanks to one of PHP's core values — maintaining backwards compatibility — old PHP 5 codebases can easily be updated to benefit from these changes.

得益于 PHP 的核心价值观之一——保持向后兼容性——旧的 PHP 5 代码库可以轻松更新以从这些变化中受益。

## What happened to 6?

版本 6 发生了什么？

PHP 5.6 was the latest version in the 5 series, with the next one being 7.0. What happened to version 6? The core team started working on it, only to realise rather late that there were major issues with the internal implementation.

PHP 5.6 是 5 系列的最新版本，下一个版本是 7.0。那么版本 6 发生了什么？核心团队开始开发它，但直到很晚才意识到内部实现存在重大问题。 

They decided to rework the engine once again, but "PHP 6" was already being written. To avoid confusion, they decided to skip version 6, and jump straight to PHP 7.

他们决定再次重新设计引擎，但"PHP 6"已经在编写中了。为了避免混淆，他们决定跳过版本 6，直接跳到 PHP 7。

The story of PHP 6 has become folklore within the community. If you want to know the in-depth story, you can do a quick Google search.Even though PHP 7.0 was such a milestone, we've since moved on from it as well.

PHP 6 的故事已经成为社区内的传说。如果你想了解深入的故事，可以快速搜索一下 Google。尽管 PHP 7.0 是一个如此重要的里程碑，但到现在 PHP 还在继续前进。 

PHP 7.0 is already considered old: it was released in 2015 and didn't receive updates anymore five years later. Around the late 5.x releases, PHP adopted a strict release cycle: every year brings one new version. Most versions are actively supported for two years, followed by one year of additional security support. After three years, you should update, as the version you are using doesn't get security patches anymore.

PHP 7.0 已经被认为是旧版本了：它于 2015 年发布，五年后不再接收更新。大约在 5.x 后期版本，PHP 采用了严格的发布周期：每年发布一个新版本。大多数版本会得到两年的积极支持，随后是一年的额外安全支持。三年后，你应该更新，因为你使用的版本不再获得安全补丁。

Arguably, it's even better to follow along with the latest version. There will always be minor breaking changes and deprecations, but most code can easily be updated.

可以说，跟随最新版本甚至更好。虽然总会有一些小的破坏性变更和弃用，但大多数代码可以轻松更新。 

There even are great automated tools that will take your existing codebase, detect any upgrading errors, and fix them automatically.

甚至还有出色的自动化工具，可以接收你现有的代码库，检测任何升级错误，并自动修复它们。

Automation One of those automated tools is called Rector which has grown in popularity over the years: https://github.com/rectorphp/rector . Rector can update your codebase automatically across several PHP versions and is a great tool to know about if you ever have to deal with legacy projects.

自动化 其中一个自动化工具叫做 Rector，这些年来它越来越受欢迎：https://github.com/rectorphp/rector。Rector 可以自动更新你的代码库，跨越多个 PHP 版本，如果你必须处理遗留项目，这是一个值得了解的好工具。

In the next few chapters, we'll take a deep dive into the features added in PHP 7 and PHP 8. Before doing that, we'll start by looking at the smaller yet significant changes in this chapter.

在接下来的几章中，我们将深入探讨 PHP 7 和 PHP 8 中添加的功能。在此之前，我们将从本章中较小但重要的变化开始。

## Trailing commas

Support for trailing commas has been added incrementally up until PHP 8.0. They are now supported in arrays, function calls, parameter lists, and closure use statements.

对尾随逗号的支持已经逐步添加到 PHP 8.0。它们现在在数组、函数调用、参数列表和闭包 use 语句中都受支持。

Trailing commas are a somewhat controversial topic among developers. Some people like them; others hate them. One argument in favour of trailing commas is that they make diffs easier. For example, imagine an array with two elements:

尾随逗号在开发者中是一个有些争议的话题。有些人喜欢它们；其他人讨厌它们。支持尾随逗号的一个论点是它们使差异更容易。例如，想象一个包含两个元素的数组：

```php
$array = [
$foo,
$bar

];

```

Next you'd need to add a third:

接下来你需要添加第三个：

```php
$array = [
$foo,
$bar,
$baz
];
```

Version control systems such as GIT would list two changes instead of one, because you really did make two actual changes. If you'd always used trailing commas, you wouldn't need to alter the existing lines:

像 GIT 这样的版本控制系统会列出两个更改而不是一个，因为你确实做了两个实际的更改。如果你总是使用尾随逗号，你就不需要修改现有行：

```php
$array = [
$foo,
$bar,
$baz,

];

```

Besides version control diffs, trailing commas can also be considered "easier" to reason about because you never have to worry about adding an extra comma or not.

除了版本控制差异之外，尾随逗号也可以被认为"更容易"推理，因为你永远不必担心是否添加额外的逗号。 

You might not prefer this writing style, and that's fine. We'll discuss the importance of a style guide in a later chapter.

你可能不喜欢这种写作风格，这没关系。我们将在后面的章节中讨论风格指南的重要性。

## Formatting numeric values
You can use an underscore to format numeric values. This underscore is completely
ignored when the code is parsed but makes long numbers easier to read by humans.

你可以使用下划线来格式化数值。这个下划线在解析代码时会被完全忽略，但使长数字更容易被人阅读。

This can be especially useful in tests. Take the following example: we're testing an invoice flow and we need to pass in an amount of money. It's a good idea to store money in cents, to prevent rounding errors, so using an _ makes it clearer:

这在测试中尤其有用。以下面的例子为例：我们正在测试发票流程，需要传入一个金额。将钱以分为单位存储是个好主意，以防止舍入错误，所以使用 _ 使其更清晰：

```php
public function test_create_invoice()

{
    // $100 and 10 cents

    $invoice = new Invoice(100_10);

    // Assertions
}

```

## Anonymous classes
Anonymous classes were added in PHP 7.0. They can be used to create objects on the fly; they can even extend a base class. Here's an example in a test context:

匿名类 匿名类在 PHP 7.0 中添加。它们可以用来即时创建对象；它们甚至可以扩展基类。以下是在测试上下文中的一个例子：

```php
public function test_dto_type_checking_with_arrays(): void
{
    $dto = new class(

        ['arrayOfInts' => [1, 2]]


    ) extends DataTransferObject {

        /** @var int[] */

        public array $arrayOfInts;

    }; 

    // Assertions
}    
```
## Flexible heredoc
Heredoc can be a useful tool for larger strings, though they had an annoying indentation quirk in the past: you couldn't have any whitespaces in front of the closing delimiter. In effect, that meant you had to do this:

Heredoc 可以是处理较大字符串的有用工具，尽管它们在过去有一个烦人的缩进怪癖：你不能在结束分隔符前面有任何空格。实际上，这意味着你必须这样做：

```php
public function report(): void
{
    $query = ==<SQL SELECT * 
        FROM `table`
        WHERE `column` = true;
SQL;

}

```

Fortunately, you can now do this:

幸运的是，你现在可以这样做：

```php
public function report(): void
{
    $query = ==<SQL SELECT * 
        FROM `table`
        WHERE `column` = true;

    SQL;
}

```

The whitespace in front of the closing marker will be ignored on all lines.

结束标记前面的空格将在所有行上被忽略。

## Exception improvements
Let's take a look at two smaller additions in PHP 8. First: a throw statement is now an expression. That means you can use it in more places, such as the null coalescing righthand operand, or in short closures; we'll cover both of those features in-depth later.

让我们看看 PHP 8 中的两个较小的添加。首先：throw 语句现在是一个表达式。这意味着你可以在更多地方使用它，例如空合并运算符的右操作数，或在短闭包中；我们稍后将深入介绍这两个功能。
```php
// Invalid before PHP 8

$name = $input['name'] =? throw new NameNotFound();

// Valid as of PHP 8

$name = $input['name'] =? throw new NameNotFound();
$error = fn (string $class) => throw new $class(); 

```

Second: exceptions support non-capturing catches. There might be cases where you want to catch an exception to keep the program flow going and not do anything with it. You always had to assign a variable to the caught exception, even when you didn't use it. That's not necessary anymore:

其次：异常支持非捕获的 catch。可能有些情况下，你想捕获异常以保持程序流程继续，但不对它做任何事情。你总是必须为捕获的异常分配一个变量，即使你不使用它。现在不再需要这样了：

```php
try {
    // Something goes wrong
} catch (Exception) {
    // Just continue
}
```
## Weak references and maps 
PHP 7.4 added the concept of weak references. To understand what they are, you need to know a little bit about garbage collection. Whenever an object is created, it requires some memory to keep track of its state. If an object is created and assigned to a variable, then that variable is a reference to the object. As soon as there are no references to an object anymore, it cannot be used, and it doesn't make sense to keep it in memory. That's why the garbage collector sometimes comes along looking for those kinds of objects and removes them, freeing memory.

PHP 7.4 添加了弱引用的概念。要理解它们是什么，你需要了解一点关于垃圾收集的知识。每当创建一个对象时，它需要一些内存来跟踪其状态。如果创建了一个对象并将其分配给变量，那么该变量就是对该对象的引用。一旦不再有对对象的引用，它就不能被使用，将其保留在内存中也没有意义。这就是为什么垃圾收集器有时会寻找这些类型的对象并删除它们，释放内存。

Weak references are references to objects which don't prevent them from being garbage collected. This feature on its own might seem a little strange, but they allow an interesting use case as of PHP 8, combined with weak maps: a map of objects which are referenced using weak references.

弱引用是对对象的引用，不会阻止它们被垃圾收集。这个功能本身可能看起来有点奇怪，但从 PHP 8 开始，它们与弱映射结合使用，允许一个有趣的用例：使用弱引用引用的对象映射。

Take the example of ORMs: they often implement caches which hold references to entity classes to improve the performance of relations between entities. These entity objects can not be garbage collected, as long as this cache has a reference to them, 

even if the cache is the only thing referencing them.

以 ORM 为例：它们经常实现缓存，这些缓存持有对实体类的引用，以提高实体之间关系的性能。只要这个缓存有对它们的引用，这些实体对象就不能被垃圾收集，即使缓存是唯一引用它们的东西。

If this caching layer uses weak references and maps instead, PHP will garbage collect these objects when nothing else references them anymore. Especially in the case of ORMs, which can manage several hundred, if not thousands of entities within a request; weak maps can offer a better, more resource-friendly way of dealing with these objects.

如果这个缓存层改用弱引用和映射，PHP 将在没有其他东西引用它们时垃圾收集这些对象。特别是在 ORM 的情况下，它们可以在一个请求中管理数百甚至数千个实体；弱映射可以提供更好、更资源友好的方式来处理这些对象。

Here's what weak maps look like:

以下是弱映射的样子：

```php
class EntityCache 

{

    public function =_construct(

        private WeakMap $cache

    ) {}

 

    public function getSomethingWithCaching(object $object): object

    {

        if (! isset($this=>cache[$object])) {
$this=>cache[$object] = $this

                =>computeSomethingExpensive($object);

        }

        return $this=>cache[$object];

    }

    

```

    // …

```php
}

```

In this example, we cache the result of an expensive operation related to an object in a cache. If the result doesn't exist yet, we'll compute it once. Thanks to weak maps, this object can still be garbage collected if there are no other references to it anymore.

在这个例子中，我们将与对象相关的昂贵操作的结果缓存在缓存中。如果结果还不存在，我们将计算一次。由于弱映射，如果不再有其他引用，这个对象仍然可以被垃圾收集。J

## The JIT
The JIT — just in time — compiler is a core mechanism added in PHP 8 which can significantly speed up PHP code.

The JIT——即时编译器——是 PHP 8 中添加的核心机制，可以显著加速 PHP 代码。

A JIT compiler will look at code while running and tries to find pieces of that code that are executed often. The compiler will take those parts and compile them to machine code — on the fly — and use the optimised machine code from then on out. The technique can be used in interpreted languages like JavaScript, and now also in PHP. It has the potential to improve an application's performance significantly.

JIT 编译器会在运行时查看代码，并尝试找到经常执行的那部分代码。编译器将获取这些部分并将它们编译为机器代码——即时编译——然后从那时起使用优化的机器代码。这种技术可以在像 JavaScript 这样的解释型语言中使用，现在也可以在 PHP 中使用。它有潜力显著提高应用程序的性能。

I say "potential" because there are a few caveats we must take into account. I'll keep those and everything else JIT-related for the chapter dedicated to the JIT.

我说"潜力"是因为我们必须考虑一些注意事项。我将把这些以及所有其他与 JIT 相关的内容保留在专门讨论 JIT 的章节中。

## Class shorthand on objects
The ::class shorthand was added in PHP 5.5 to quickly get the full class name of an
imported one:

对象上的类简写 =:class 简写在 PHP 5.5 中添加，用于快速获取导入类的完整类名：

```php
$className = Offer=:class;

```

In PHP 8 this also works with variables:

在 PHP 8 中，这也适用于变量：

```php
$className = $offer=:class;

```

## Improved string to number comparisons

One of PHP's dynamic type system strengths is one of its weaknesses at the same
time: type juggling. PHP will try to change a variable's type when it encounters a
strange piece of code. Here's an example where strings and numbers are compared:

改进的字符串到数字比较 PHP 动态类型系统的优势之一同时也是它的弱点之一：类型转换。当 PHP 遇到一段奇怪的代码时，它会尝试更改变量的类型。以下是一个比较字符串和数字的例子：
```
'1' == 1 // true 
```

If you don't want this type juggling, you'd use the triple === sign instead:
如果你不想要这种类型转换，你可以使用三个 === 符号代替：
```
'1' === 1 // false 
```

There are strange edge cases when using weak comparisons, though. The following
returns true in versions before PHP 8:

然而，使用弱比较时有一些奇怪的边缘情况。以下在 PHP 8 之前的版本中返回 true：
```
'foo' == 1 // true
```

As of PHP 8, this behaviour is improved. The example above, as well as other edge
cases, would now return false correctly.

从 PHP 8 开始，这种行为得到了改进。上面的例子以及其他边缘情况现在会正确返回 false。

```
'foo' == 1 // false
```

## Changes to the error control operator 
One last notable change is that the @ operator no longer silences fatal errors. You can still use it to silence other kinds of errors, like so:

最后一个值得注意的变化是 @ 运算符不再抑制致命错误。你仍然可以使用它来抑制其他类型的错误，像这样：

```php
$file = @file_get_contents('none/existing/path');

```

In cases where you don't use the @ operator, an error would be triggered, but with @, $file  will simply be false. If, on the other hand, a fatal error is thrown in PHP 8, the @ operator wouldn't ignore it anymore.

在你不使用 @ 运算符的情况下，会触发错误，但使用 @ 时，$file 将简单地是 false。另一方面，如果在 PHP 8 中抛出致命错误，@ 运算符将不再忽略它。

## Deep down in the core
There are two low-level components added to PHP's core with the 7.4 update: FFI and
preloading. These are two complex topics on their own, each with their own chapter.
I'll briefly mention them here, though.

在 7.4 更新中，PHP 核心添加了两个底层组件：FFI 和预加载。这是两个复杂的主题，各自都有自己的章节。 不过，我会在这里简要提及它们。

FFI — a.k.a. foreign function interface — allows PHP to speak to shared libraries written in, for example C, directly. To put that in other words: it's possible to write PHP extensions and ship them as composer packages without installing the low-level PHP extensions themselves. I promise we'll dive deeper into this soon!

FFI——也称为外部函数接口——允许 PHP 直接与用例如 C 编写的共享库通信。换句话说：可以编写 PHP 扩展并将它们作为 composer 包分发，而无需安装底层 PHP 扩展本身。我保证我们很快就会深入探讨这个！

The other one — preloading — enables you to compile PHP code on server startup. 
That code will be kept in memory for all subsequent requests. It can speed up your average PHP web framework since it doesn't have to boot anymore on every request.

另一个——预加载——使你能在服务器启动时编译 PHP 代码。该代码将保留在内存中，供所有后续请求使用。它可以加速你的平均 PHP Web 框架，因为它不再需要在每个请求上启动。 

Again: this one deserves a chapter on its own.

再次：JIT 值得单独用一章来深入了解。

So with these random little features out of the way, let's dig deeper into all great things added to PHP over the past years!

所以，把这些零散的小功能放在一边，让我们深入探讨过去几年添加到 PHP 的所有伟大功能！
