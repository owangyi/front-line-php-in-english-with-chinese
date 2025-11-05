# Chapter 2: New Versions

Since this book aims to bring you up to speed with modern PHP practices, it's im-

为了让你快速把握现代 PHP 的实践，有必要先搞清楚近十年来语言本身发生了什么变化。自从 PHP 7 的开发与发布开始，PHP 的生态与面貌发生了巨大的变化。我更愿意把 7.x 系列看作这门语言的“成熟期”，就从这里说起。

portant to know what happened to the language over the past decade or so. With the

首先，PHP 7.0 带来了显著的性能提升。内核大量重写，带来肉眼可见的差异。仅仅切换到 PHP 7 或更高版本，你的应用经常就能获得 2～3 倍的速度提升。得益于 PHP 坚守的“向后兼容”价值观，许多旧的 PHP 5 代码库可以较为容易地升级并享受这些红利。

development and release of PHP 7, the PHP landscape changed dramatically. I like to

关于“6 到哪去了？”：PHP 5.6 是 5 系列的最后一个版本，理论上后续应是 6。但核心团队在推进 6 的过程中，较晚地意识到内部实现存在重大问题，于是决定再次重做引擎。那时“PHP 6”这个名字已在市面上被使用，为避免混乱，大家决定跳过 6，直接发布 PHP 7。这个故事如今几乎成了社区传说。

think of the PHP 7.x versions as a maturity phase for the language, so this is where we

虽然 7.0 是里程碑，但它也已成为过去：2015 年发布，五年后停止更新。自 5.x 末期起，PHP 采用了严格的节奏：基本每年一个大版本。大多数版本会获得 2 年的主动支持，再加 1 年的安全支持。也就是说，3 年后应当升级，否则将不再获得安全补丁。

will start.

从实践角度看，最好尽量跟随最新稳定版本。每个版本都会有一些小的破坏性变更与弃用，但大部分代码都可以较容易地升级。并且已经有很棒的自动化工具可以帮你扫描并修复升级问题（例如 Rector）。

First and foremost, PHP 7.0 comes with a significant performance boost. Much of

在接下来的几章里，我们会深入介绍 PHP 7 与 PHP 8 的核心特性。在此之前，先看一些更小但同样重要的变化。

PHP's core was rewritten, which resulted in a noticeable difference. It's not uncommon

直到 PHP 8.0，尾随逗号的支持是逐步加入的：现在可用于数组、函数调用、参数列表以及闭包的 use 语句。是否使用尾随逗号常引发争议，但一个支持它的理由是能让 diff 更清晰，且减少修改已有行的必要。

to see your application run two or three times as fast, just by using PHP 7 or higher.

示例（代码保持原样）：

Thanks to one of PHP's core values — maintaining backwards compatibility — old PHP

你可以用下划线来分隔数字以提升可读性。下划线在解析时会被忽略。（示例略）

5 codebases can easily be updated to benefit from these changes.

现在允许在 heredoc/nowdoc 的结束标记前保留缩进，解析器会自动忽略对应的前导空白。

What happened to 6?

示例（代码保持原状）：

PHP 5.6 was the latest version in the 5 series, with the next one being 7.0. What

- throw 变为表达式：可以用于更多位置（例如空合并表达式的右操作数、短闭包内等）。
- 非捕获式 catch：允许不绑定异常变量，仅用于“吞掉”异常以继续流程。

happened to version 6? The core team started working on it, only to realise

示例（代码保持原状）：

rather late that there were major issues with the internal implementation.

PHP 7.4 引入弱引用（weak references），PHP 8 引入 WeakMap。弱引用不会阻止对象被 GC 回收；WeakMap 则允许用弱引用作为键来缓存与对象相关的计算结果。典型用例是在 ORM 中缓存实体关系的结果，同时避免因为缓存而长期占用内存。

They decided to rework the engine once again, but "PHP 6" was already being

示例（代码保持原状）：

written. To avoid confusion, they decided to skip version 6, and jump straight to

PHP 8 加入了 JIT，即“即时编译”。它会在运行时寻找热点代码，并将其即时编译为机器码，以期提升执行效率。JIT 对典型 Web I/O 负载的应用提升有限，但在计算密集型场景（如数据处理、图像/音视频编解码、科学计算等）可能带来更明显的收益。后续章节会专门讨论 JIT。

PHP 7.

PHP 的“弱比较”（==）会发生类型转换，容易导致边界行为。在 PHP 8 之前，诸如 `'foo' == 1` 这样的比较会得到 true。PHP 8 修正了这些异常边界：

The story of PHP 6 has become folklore within the community. If you want to

`@` 不再抑制致命错误（fatal error）。它依旧可以抑制非致命错误，例如：

know the in-depth story, you can do a quick Google search.

若发生致命错误，`@` 将不再生效。

14

- FFI（外部函数接口）：允许 PHP 直接调用如 C 语言编写的共享库，从而以 Composer 包的形式分发“扩展级”能力，而无需安装传统的底层扩展。
- 预加载（preloading）：在服务器启动时预编译并将代码常驻内存，减少每次请求的框架启动开销。这两个主题会在后文单独成章详述。

Even though PHP 7.0 was such a milestone, we've since moved on from it as well.

以上是本章的若干“零散但重要”的改进。接下来，我们将深入介绍过去几年为 PHP 带来的更大变化与新能力。

PHP 7.0 is already considered old: it was released in 2015 and didn't receive updates

anymore five years later. Around the late 5.x releases, PHP adopted a strict release

cycle: every year brings one new version. Most versions are actively supported for

two years, followed by one year of additional security support. After three years, you

should update, as the version you are using doesn't get security patches anymore.

Arguably, it's even better to follow along with the latest version. There will always

be minor breaking changes and deprecations, but most code can easily be updated.

There even are great automated tools that will take your existing codebase, detect

any upgrading errors, and fix them automatically.

Automation

One of those automated tools is called Rector which has grown in popularity

over the years: https://github.com/rectorphp/rector. Rector can update your

codebase automatically across several PHP versions and is a great tool to know

about if you ever have to deal with legacy projects.

In the next few chapters, we'll take a deep dive into the features added in PHP 7 and

PHP 8. Before doing that, we'll start by looking at the smaller yet significant changes

in this chapter.

Chapter 02 - New Versions

Trailing commas

Support for trailing commas has been added incrementally up until PHP 8.0. They are

now supported in arrays, function calls, parameter lists, and closure use statements.

Trailing commas are a somewhat controversial topic among developers. Some people

like them; others hate them. One argument in favour of trailing commas is that they

make diffs easier. For example, imagine an array with two elements:

$array = [

$foo,

$bar

];

Next you'd need to add a third:

$array = [

$foo,

$bar,

$baz

];

16

Version control systems such as GIT would list two changes instead of one, because

you really did make two actual changes. If you'd always used trailing commas, you

wouldn't need to alter the existing lines:

$array = [

$foo,

$bar,

$baz,

];

Besides version control diffs, trailing commas can also be considered "easier" to

reason about because you never have to worry about adding an extra comma or not.

You might not prefer this writing style, and that's fine. We'll discuss the importance of

a style guide in a later chapter.

Formatting numeric values

You can use an underscore to format numeric values. This underscore is completely

ignored when the code is parsed but makes long numbers easier to read by humans.

Chapter 02 - New Versions

This can be especially useful in tests. Take the following example: we're testing an

invoice flow and we need to pass in an amount of money. It's a good idea to store

money in cents, to prevent rounding errors, so using an _ makes it clearer:

public function test_create_invoice()

{

// $100 and 10 cents

$invoice = new Invoice(100_10);

// Assertions

}

Anonymous classes

Anonymous classes were added in PHP 7.0. They can be used to create objects on the

fly; they can even extend a base class. Here's an example in a test context:

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

18

Flexible heredoc

Heredoc can be a useful tool for larger strings, though they had an annoying indenta-

tion quirk in the past: you couldn't have any whitespaces in front of the closing delim-

iter. In effect, that meant you had to do this:

public function report(): void

{

$query = ==<SQL

SELECT *

FROM `table`

WHERE `column` = true;

SQL;

// …

}

Fortunately, you can now do this:

public function report(): void

{

$query = ==<SQL

SELECT *

FROM `table`

WHERE `column` = true;

SQL;

// …

}

The whitespace in front of the closing marker will be ignored on all lines.

Chapter 02 - New Versions

Exception improvements

Let's take a look at two smaller additions in PHP 8. First: a throw statement is now

an expression. That means you can use it in more places, such as the null coalescing

righthand operand, or in short closures; we'll cover both of those features in-depth

later.

// Invalid before PHP 8

$name = $input['name'] =? throw new NameNotFound();

// Valid as of PHP 8

$name = $input['name'] =? throw new NameNotFound();

$error = fn (string $class) => throw new $class();

Second: exceptions support non-capturing catches. There might be cases where you

want to catch an exception to keep the program flow going and not do anything with

it. You always had to assign a variable to the caught exception, even when you didn't

use it. That's not necessary anymore:

try {

// Something goes wrong

} catch (Exception) {

// Just continue

}

20

Weak references and maps

PHP 7.4 added the concept of weak references. To understand what they are, you

need to know a little bit about garbage collection. Whenever an object is created, it

requires some memory to keep track of its state. If an object is created and assigned

to a variable, then that variable is a reference to the object. As soon as there are no

references to an object anymore, it cannot be used, and it doesn't make sense to keep

it in memory. That's why the garbage collector sometimes comes along looking for

those kinds of objects and removes them, freeing memory.

Weak references are references to objects which don't prevent them from being

garbage collected. This feature on its own might seem a little strange, but they allow

an interesting use case as of PHP 8, combined with weak maps: a map of objects

which are referenced using weak references.

Take the example of ORMs: they often implement caches which hold references to

entity classes to improve the performance of relations between entities. These entity

objects can not be garbage collected, as long as this cache has a reference to them,

even if the cache is the only thing referencing them.

If this caching layer uses weak references and maps instead, PHP will garbage collect

these objects when nothing else references them anymore. Especially in the case

of ORMs, which can manage several hundred, if not thousands of entities within a

request; weak maps can offer a better, more resource-friendly way of dealing with

these objects.

Chapter 02 - New Versions

Here's what weak maps look like:

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

// …

}

In this example, we cache the result of an expensive operation related to an object

in a cache. If the result doesn't exist yet, we'll compute it once. Thanks to weak

maps, this object can still be garbage collected if there are no other references to it

anymore.

22

The JIT

The JIT — just in time — compiler is a core mechanism added in PHP 8 which can

significantly speed up PHP code.

A JIT compiler will look at code while running and tries to find pieces of that code that

are executed often. The compiler will take those parts and compile them to machine

code — on the fly — and use the optimised machine code from then on out. The tech-

nique can be used in interpreted languages like JavaScript, and now also in PHP. It has

the potential to improve an application's performance significantly.

I say "potential" because there are a few caveats we must take into account. I'll keep

those and everything else JIT-related for the chapter dedicated to the JIT.

Class shorthand on objects

The =:class shorthand was added in PHP 5.5 to quickly get the full class name of an

imported one:

$className = Offer=:class;

In PHP 8 this also works with variables:

$className = $offer=:class;

Chapter 02 - New Versions

Improved string to number comparisons

One of PHP's dynamic type system strengths is one of its weaknesses at the same

time: type juggling. PHP will try to change a variable's type when it encounters a

strange piece of code. Here's an example where strings and numbers are compared:

'1' == 1 // true

If you don't want this type juggling, you'd use the triple === sign instead:

'1' === 1 // false

There are strange edge cases when using weak comparisons, though. The following

returns true in versions before PHP 8:

'foo' == 1 // true

As of PHP 8, this behaviour is improved. The example above, as well as other edge

cases, would now return false correctly.

'foo' == 1 // false

24

Changes to the error control operator

One last notable change is that the @ operator no longer silences fatal errors. You can

still use it to silence other kinds of errors, like so:

$file = @file_get_contents('none/existing/path');

In cases where you don't use the @ operator, an error would be triggered, but with @,

$file will simply be false. If, on the other hand, a fatal error is thrown in PHP 8, the @

operator wouldn't ignore it anymore.

Deep down in the core

There are two low-level components added to PHP's core with the 7.4 update: FFI and

preloading. These are two complex topics on their own, each with their own chapter.

I'll briefly mention them here, though.

FFI — a.k.a. foreign function interface — allows PHP to speak to shared libraries

written in, for example C, directly. To put that in other words: it's possible to write PHP

extensions and ship them as composer packages without installing the low-level PHP

extensions themselves. I promise we'll dive deeper into this soon!

The other one — preloading — enables you to compile PHP code on server startup.

That code will be kept in memory for all subsequent requests. It can speed up your

average PHP web framework since it doesn't have to boot anymore on every request.

Again: this one deserves a chapter on its own.

So with these random little features out of the way, let's dig deeper into all great

things added to PHP over the past years!

