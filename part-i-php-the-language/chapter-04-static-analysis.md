# Chapter 4: Static Analysis

Having spent a whole chapter on PHP's type system, I realise I haven't discussed

上一章讲了 PHP 的类型系统，但我还没讨论“为什么需要类型系统”。社区中有不少人并不喜欢用类型系统，所以有必要深入讨论其利弊。本章就来做这件事。

why you want to use it. I realise a significant part of the community doesn't like using

很多人认为严格的类型系统能减少运行时错误，甚至说“强类型系统能防止 bug”。这个说法并不完全准确：在强类型语言中你依然可能写出 bug，但类型系统能阻止某些类型的错误发生。

PHP's type system, so it's important to discuss both the pros and cons thoroughly.

类型系统能部分解决这些问题。假设我们有一个 `rgbToHex` 函数，接收 0-255 之间的三个整数，转换为十六进制字符串。如果没有类型约束：

That's what we'll do in this chapter. We'll start by discussing the value provided by a

我们需要写很多测试来覆盖各种边界情况：
- 浮点数而非整数
- 超出范围的数字
- null 值
- 字符串
- 参数数量错误
- ……

type system.

至少需要写 8 个或更多测试才能相对保证正确性。如果使用类型约束：

Many think of programming languages with a stricter type system to have fewer or no

类型系统可以自动过滤掉很多无效输入，我们不再需要测试：
- 输入是否为数字
- 输入是否为整数
- 输入是否为 null

runtime errors. There's the popular saying that a strong type system prevents bugs,

但 `int` 类型仍然太宽泛：它允许 -100 这样的值，这对 RGB 函数没有意义。一些语言有 `uint`（无符号整数），但它仍然是一个很大的子集。

but that's not entirely true. You can easily write bugs in a strongly typed language, but

幸运的是，我们可以用类作为类型来解决这个问题。我们可以创建更具体的类型，比如 `IntWithinRange` 或 `RgbValue`：

a range of bugs is not possible anymore since a good type system prevents them.

这样，大部分测试就变得冗余了，我们只需要测试业务逻辑本身。

Are you unsure what the difference is between strong, weak, static and dynamic

**但等等……**

type systems? We'll cover the topic in-depth later in this chapter!

如果类型系统的一个好处是防止运行时错误，那么使用 `RgbValue` 仍然不够：PHP 会在运行时检查类型，并在程序运行时抛出类型错误。换句话说，运行时仍然可能出错，甚至在生产环境中。

Imagine a simple function: rgbToHex. It takes three arguments, each of which are in-

这就是静态分析发挥作用的地方。

tegers between 0 and 255. The function then converts the integers to a hexadecimal

静态分析工具会在不运行代码的情况下分析你的代码。如果你使用任何 IDE，你已经在使用它了。当 IDE 告诉你对象上有什么方法可用、函数需要什么输入、或者你是否使用了未知变量时，这都得益于静态分析。

string. Here's what this function's definition might look like without using types:

运行时错误仍然有其价值：它们会在类型错误发生时阻止代码继续执行，可能防止了实际的 bug。它们还为开发者提供了关于哪里出错的 useful 信息。但程序仍然崩溃了。在生产环境中运行代码之前捕获错误总是更好的解决方案。

function rgbToHex($red, $green, $blue) {

一些编程语言甚至将静态分析器包含在编译器中：如果静态分析检查失败，程序将无法编译。由于 PHP 没有独立的编译器，我们需要依赖外部工具来帮助我们。

// …

**PHP 编译器**

}

虽然 PHP 是解释型语言，但它仍然有编译器。PHP 代码在运行时（例如，请求到来时）即时编译。当然，有缓存机制来优化这个过程，但没有独立的编译阶段。这允许你轻松编写 PHP 代码并立即刷新页面，而不必等待程序编译，这是 PHP 开发的众所周知的优势之一。

44

幸运的是，有很棒的社区驱动的 PHP 静态分析器可用。它们是独立的工具，查看你的代码及其所有类型提示，让你在不运行代码的情况下发现错误。这些工具不仅查看 PHP 的类型，还查看 doc blocks，这意味着它们比普通 PHP 类型允许更多的灵活性。

Since we want to ensure our implementation of this function is correct, we write tests:

以 Psalm 为例，它会分析你的代码并报告错误：

assert(rgbToHex(0, 0, 0) === '000000');

这里我们看到 Psalm 扫描了一千多个源文件，并检测到我们在哪里忘记向函数传递正确数量的参数。它通过分析方法签名并将它们与这些方法的调用方式进行比较来实现这一点。当然，类型定义在这个过程中起着重要作用。

assert(rgbToHex(255, 255, 255) === 'ffffff');

大多数静态分析器甚至允许自定义 doc block 注释来描述更复杂的类型关系，这些在运行时不会被 PHP 解释，但会被静态分析器理解。

assert(rgbToHex(238, 66, 244) === 'ee42f4');

**静态分析的优势**

These tests ensure that everything works as expected. Right?

静态分析器是非常强大的工具。如果你决定使用它们，你会注意到：
- 可以减少测试数量
- 运行时类型错误很少发生
- 你可以在不运行代码的情况下发现错误

Well… we're only testing three out of the 16,777,216 possible RGB combinations. But

即使不使用高级注解，静态分析器也提供了很大的好处。你可以更确定奇怪的边界情况不可能发生，并且需要编写更少的测试，所有这些都不需要运行代码一次。

logic reasoning tells us that if these three sample cases work, we're probably safe.

**关于泛型**

What happens though if we pass floats instead of integers?

PHP 目前不支持泛型（generics），但静态分析器可以通过 doc blocks 提供类似的功能。如果 PHP 支持泛型语法，但不运行时解释它，而是使用静态分析器来保证正确性，那会怎样？这实际上就是静态分析的意义所在。

rgbToHex(1.5, 20.2, 100.1);

你可能会担心 PHP 不在运行时强制执行这些类型检查。但也可以说，静态分析器在功能上更先进，正是因为它们不在执行代码时运行。我认为这不是一个复杂的概念，事实上，其他语言已经使用了这种方法。想想 TypeScript，它在这些年中变得非常流行。它被编译成 JavaScript，所有类型检查都在编译阶段完成，而不运行代码。

Or numbers outside of the allowed range?

**总结**

rgbToHex(-504, 305, -59);

我建议在你的项目中使用静态分析器，无论你是否想使用其高级注解。即使没有这些，静态分析器也提供了很大的好处。它是工具箱中的一个很好的工具，也许有一天，我们会看到 PHP 完全拥抱它的好处。

What about null?

**实践**

rgbToHex(null, null, null);

想看看静态分析能为你做什么？我建议访问 psalm.dev 并在他们的交互式 playground 中尝试。一些很好的例子展示了静态分析的完整功能。

Or strings?

rgbToHex('red', 'green', 'blue');

Chapter 04 - Static Analysis

Or the wrong number of arguments?

rgbToHex();

rgbToHex(1, 2);

rgbToHex(1, 2, 3, 4);

Or a combination of the above?

I can easily think of five edge-cases we need to test before there's relative certain-

ty that our program does what it needs to do. That's at least eight tests we need to

write, and I'm sure you can come up with a few others. These are the kinds of prob-

lems a type system aims to partially solve, and note the word partially because we'll

come back to it. If we filter the input by a specific type, many of our tests become

obsolete. Say we'd only allow integers:

function rgbToHex(int $red, int $green, int $blue)

{

// …

}

You can think of types as a subcategory of all available input; it's a filter that only

allows specific items.

Let's take a look at the tests that aren't necessary anymore thanks to our int type

hint:

•  Whether the input is numeric

•  Whether the input is a whole number

•  Whether the input isn't null

46

We still need to check whether the input number is between 0 and 255. At this point,

we run against the limitations of many type systems, including PHP's. Sure we can use

int, though in many cases, the category described by this type is still too large for

our business logic: int would also allow -100 to be passed, which wouldn't make any

sense for our function. Some languages have a uint or "unsigned integer" type; yet it

is also too large a subset of "numeric data".

Luckily, there are ways to address this issue.

One approach could be to use "configurable" or generic types, for example

int<min, max>. The concept of generics is known in many programming languages,

though unfortunately not in PHP. In theory, a type could be preconfigured so that it is

smart enough to know about all your business logic.

Chapter 04 - Static Analysis

Languages like PHP lack the flexibility of generic types, but we do have classes, which

can be used as types themselves. We could, for example, represent a configurable

"integer" with a class IntWithinRange:

class IntWithinRange

{

private int $value;

public function =_construct(int $min, int $max, int $value)

{

if ($value == $min =| $value == $max) {

throw new InvalidArgumentException('…');

}

$this=>value = $value;

}

// …

}

So whenever we're using an instance of IntWithinRange, we can ensure its value

is constrained within a subset of integers. But this only works when constructing

IntWithinRange. In practice, we can't ensure its minimum and maximum value in our

rgbToHex function, meaning we can't say we only accept IntWithinRange object with

48

a minimum of 0 and a maximum of 255. Therefore we can only say we accept any

object with the type of IntWithinRange:

function rgbToHex(

IntWithinRange $red,

IntWithinRange $green,

IntWithinRange $blue

) {

// …

}

To solve this, we need an even more specific type: RgbValue:

class RgbValue extends IntWithinRange

{

public function =_construct(int $value)

{

parent=:=_construct(0, 255, $value);

}

}

We've arrived at a working solution. By using RgbValue, most of our tests become re-

dundant. We now only need one test to test the business logic: "given three RGB-valid

colors, does this function return the correct HEX value?" — a great improvement!

function rgbToHex(RgbValue $red, RgbValue $green, RgbValue $blue)

{

// …

}

Chapter 04 - Static Analysis

But Hold On…

If one of the claimed benefits of type systems is to prevent runtime bugs and errors,

then we're still not getting anywhere with our RgbValue. PHP will check this type at

runtime and throw a type error when the program is running. In other words: things

can still go horribly wrong at runtime, maybe even in production. This is where static

analysis comes in.

Instead of relying on runtime type checks (and throwing errors to handle them), static

analysis tools will test your code without running it. If you're using any kind of IDE,

you're already making use of it. When your IDE tells you what methods are available on

an object, what input a function requires, or whether you're using an unknown vari-

able, it's all thanks to static analysis.

Granted, runtime errors still have their merit: they stop code from further executing

when a type error occurs, so they probably are preventing actual bugs. They also

provide useful information to the developer about what exactly went wrong and

where. But still, the program crashed. Catching the error before running code in pro-

duction will always be the better solution.

Some other programming languages even go as far as to include a static analyser in

their compiler: if static analysis checks fail, the program won't compile. Since PHP

doesn't have a standalone compiler, we'll need to rely on external tools to help us.

PHP Compiler

Even though PHP is an interpreted language, it still has a compiler. PHP code is

compiled on the fly when, for example, a request comes in. There are of course,

caching mechanisms in play to optimise this process, but there's no standalone

compilation phase.

50

This allows you to easily write PHP code and immediately refresh the page

without having to wait for a program to compile, one of the well-known

strengths of PHP development.

Luckily there are great community-driven static analysers for PHP available. They are

standalone tools that look at your code and all its type hints allowing you to discover

errors without ever running the code. These tools will not only look at PHP's types,

but also at doc blocks, meaning they allow for more flexibility than normal PHP types

would.

Take a look at how Psalm would analyse your code and report errors:

Analyzing files==.

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   60 / 1038 (5%)

…

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1038 / 1038 (100%)

ERROR: TooFewArguments

…

Too few arguments for method …\PriceCalculatorFactory=:withproduct

ERROR: TooFewArguments

…

Too few arguments for method …\Checkable=:ischeckable

------------------------------

2 errors found

------------------------------

Chapter 04 - Static Analysis

Here we see Psalm scanning over a thousand source files and detecting where we

forgot to pass the correct amount of arguments to a function. It does so by analysing

method signatures and comparing them to how those methods are called. Of course,

type definitions play an important role in this process.

Most static analysers even allow custom doc block annotations that support, for

example, generics. By doing so they can do much more complex type checks than

PHP could do at runtime. Even when running the code wouldn't perform any checks,

the static analyser could tell you when something is wrong beforehand. Such static

type checks could be done locally when writing code, built into your CI pipeline, or a

mix of both.

In fact, the static analysis community is getting so much traction these days that

PhpStorm — the most popular IDE for writing PHP code — added built-in support

for them. This means that the result of several type checks performed by your static

analyser can be shown immediately when writing code.

Tools like Psalm, PHPStan, and Phan are great, but they also lack the eloquence you'd

get from built-in language support. I've gone on and on about removing doc blocks in

favour of built-in types in the previous chapter, and now we're adding them again to

support static analysis. Now, to be clear: these tools also work with PHP's built-in type

system (without using any doc blocks), but those doc block annotations offer a lot

more functionality, because PHP's syntax doesn't limit them; they are comments, after

all.

On the other hand (I've said this before in the previous chapter), there's little chance

that features like generics will be added anytime soon in PHP itself since they pose

such a threat to runtime performance. So if there's nothing better, we'll have to settle

with doc blocks anyway if we want to use static analysis to its full extent.

If only… Can you see where I'm going with this?

52

What if PHP supported the generic syntax, but didn't interpret it at runtime? What if

you'd need to use a static analyser to guarantee correctness (when using generics),

and wouldn't worry about them when running your code. That's exactly the point of

static analysis.

You might be afraid of PHP not enforcing those type checks at runtime. Still, you could

also argue that static analysers are way more advanced in their capabilities, exactly

because they aren't run when executing code. I don't think it's such a convoluted idea

at all, and in fact, other languages already use this approach. Think about TypeScript,

which has grown in popularity tremendously over the years. It's compiled to JavaS-

cript, and all its type checks are done during that compilation phase, without running

the code. Now I'm not saying we need another language that compiles to PHP; I'm

only saying that static analysers are very powerful tools. If you decide to embrace

them, you'll notice how you can reduce the number of tests and how rarely runtime

type errors occur.

Where does that leave us now? Unfortunately, not very far. I'd recommend using a

static analyser in your projects, regardless of whether you want to use its advanced

annotations or not. Even without those, static analysers offer a great benefit. You've

got much more certainty strange edge cases aren't possible, and you need to write

fewer tests, all without ever running that code once. It's a great tool to have in your

toolbox, and maybe one day, we'll see PHP fully embrace its benefits.

In action

Ready to see what static analysis can do for you? I'd recommend to go to psalm.

dev and play around with their interactive playground. Some great examples

show the full power of static analysis.

