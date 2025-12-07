# CHAPTER 04

## STATIC ANALYSIS

Having spent a whole chapter on PHP's type system, I realise I haven't discussed why you want to use it. I realise a significant part of the community doesn't like using PHP's type system, so it's important to discuss both the pros and cons thoroughly. 

在花费了整整一章讨论 PHP 的类型系统之后，我意识到我还没有讨论为什么你想要使用它。我意识到社区中有相当一部分人不喜欢使用 PHP 的类型系统，所以彻底讨论其优缺点是很重要的。

That's what we'll do in this chapter. We'll start by discussing the value provided by a type system.

这就是我们在本章中要做的事情。我们将从讨论类型系统提供的价值开始。

Many think of programming languages with a stricter type system to have fewer or no runtime errors. There's the popular saying that a strong type system prevents bugs, but that's not entirely true. You can easily write bugs in a strongly typed language, but a range of bugs is not possible anymore since a good type system prevents them.

许多人认为具有更严格类型系统的编程语言会有更少或没有运行时错误。有一个流行的说法是，强类型系统可以防止 bug，
但这并不完全正确。你仍然可以在强类型语言中轻松地写出 bug，但连着一系列的 bug 不太可能发生，因为好的类型系统会阻止它们。

Are you unsure what the difference is between strong, weak, static and dynamic type systems? We'll cover the topic in-depth later in this chapter!

你是否不确定强类型、弱类型、静态类型和动态类型系统之间的区别？我们将在本章后面深入讨论这个话题！

Imagine a simple function: rgbToHex. It takes three arguments, each of which are integers between 0 and 255. The function then converts the integers to a hexadecimal string. Here's what this function's definition might look like without using types:

想象一个简单的函数：rgbToHex。它接受三个参数，每个参数都是 0 到 255 之间的整数。该函数然后将这些整数转换为十六进制字符串。以下是不使用类型时这个函数可能的样子：

```php
function rgbToHex($red, $green, $blue) {

    // …
}
```
Since we want to ensure our implementation of this function is correct, we write tests:

由于我们想确保这个函数的实现是正确的，我们编写测试：

```php
assert(rgbToHex(0, 0, 0) === '000000');

assert(rgbToHex(255, 255, 255) === 'ffffff');

assert(rgbToHex(238, 66, 244) === 'ee42f4');

```

These tests ensure that everything works as expected. Right?

这些测试确保它可以按预期工作。对吧？

Well… we're only testing three out of the 16,777,216 possible RGB combinations. But logic reasoning tells us that if these three sample cases work, we're probably safe. 

嗯……我们只测试了 16,777,216 种可能的 RGB 组合中的三种。但逻辑推理告诉我们，如果这三个示例案例有效，我们可能是安全的。

What happens though if we pass floats instead of integers?

但是，如果我们传递浮点数而不是整数会发生什么？

```php
rgbToHex(1.5, 20.2, 100.1);

```

Or numbers outside of the allowed range?

或者超出允许范围的数字？

```php
rgbToHex(-504, 305, -59);

```

What about null ?

`null` 呢？

```php
rgbToHex(null, null, null);

```

Or strings?

或者字符串

```php
rgbToHex('red', 'green', 'blue');

```

Or the wrong number of arguments?

又或者数量错误？

```php
rgbToHex();

rgbToHex(1, 2);

rgbToHex(1, 2, 3, 4);

```

Or a combination of the above?

或者以上几种情况的组合？

I can easily think of five edge-cases we need to test before there's relative certainty that our program does what it needs to do. That's at least eight tests we need to write, and I'm sure you can come up with a few others. These are the kinds of problems a type system aims to partially solve, and note the word partially because we'll come back to it. If we filter the input by a specific type, many of our tests become obsolete. Say we'd only allow integers:

我可以轻松想到五个边界情况，我们需要在相对确定我们的程序能够完成它需要做的事情之前进行测试。这意味着我们至少需要编写八个测试，我相信你还能想出其他一些。这些就是类型系统旨在部分解决的问题，注意"部分"这个词，因为我们稍后会回到这个问题。如果我们通过特定类型过滤输入，我们的许多测试就会变得过时。假设我们只允许整数：

```php
function rgbToHex(int $red, int $green, int $blue) 

{

}

```

You can think of types as a subcategory of all available input; it's a filter that only allows specific items.

你可以将类型视为所有可用输入的子类别；它是一个只允许特定项的过滤器。

Let's take a look at the tests that aren't necessary anymore thanks to our int type hint:

• Whether the input is numeric

• Whether the input is a whole number

• Whether the input isn't null

让我们看看由于我们的 int 类型提示而不再需要的测试：

• 输入是否为数字
• 输入是否为整数
• 输入是否不为 null

We still need to check whether the input number is between 0 and 255. At this point, we run against the limitations of many type systems, including PHP's. Sure we can use int, though in many cases, the category described by this type is still too large for our business logic: int would also allow -100  to be passed, which wouldn't make any sense for our function. Some languages have a uint  or "unsigned integer" type; yet it is also too large a subset of "numeric data".

我们仍然需要检查输入数字是否在 0 到 255 之间。在这一点上，我们遇到了许多类型系统（包括 PHP 的）的限制。当然我们可以使用 int，但在许多情况下，这种类型描述的类别对我们的业务逻辑来说仍然太大：int 也会允许传递 -100，这对我们的函数来说没有任何意义。一些语言有 uint 或"无符号整数"类型；但它仍然是"数值数据"的一个太大的子集。

Luckily, there are ways to address this issue.

幸运的是，有方法可以解决这个问题。

One approach could be to use "configurable" or generic types, for example int<min, max> . The concept of generics is known in many programming languages, though unfortunately not in PHP. In theory, a type could be preconfigured so that it is smart enough to know about all your business logic.

一种方法可能是使用"可配置的"或泛型类型，例如 int<min, max>。泛型的概念在许多编程语言中都是已知的，但不幸的是，PHP 中没有。理论上，类型可以被预配置，使其足够智能，能够了解你的所有业务逻辑。

Languages like PHP lack the flexibility of generic types, but we do have classes, which can be used as types themselves. We could, for example, represent a configurable "integer" with a class IntWithinRange :

像 PHP 这样的语言缺乏泛型类型的灵活性，但我们有类，它们本身可以用作类型。例如，我们可以用一个类 IntWithinRange 来表示一个可配置的 "整数"：

```php
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

```

So whenever we're using an instance of IntWithinRange , we can ensure its value is constrained within a subset of integers. But this only works when constructing IntWithinRange . In practice, we can't ensure its minimum and maximum value in our rgbToHex  function, meaning we can't say we only accept IntWithinRange  object witha minimum of 0 and a maximum of 255. Therefore we can only say we accept any object with the type of IntWithinRange :

因此，每当我们使用 IntWithinRange 的实例时，我们可以确保其值被限制在整数的子集内。但这只在构造 IntWithinRange 时有效。在实践中，我们无法在 rgbToHex 函数中确保其最小值和最大值，这意味着我们不能说我们只接受最小值为 0、最大值为 255 的 IntWithinRange 对象。因此，我们只能说我们接受任何 IntWithinRange 类型的对象：

```php
function rgbToHex(

```

    IntWithinRange $red, 

    IntWithinRange $green, 

    IntWithinRange $blue

) {
    // …
}

```

To solve this, we need an even more specific type: RgbValue :

为了解决这个问题，我们需要一个更具体的类型：RgbValue：

```php
class RgbValue extends IntWithinRange

{

    public function =_construct(int $value) 

    {

        parent::__construct(0, 255, $value);

    }

}

```

We've arrived at a working solution. By using RgbValue , most of our tests become redundant. We now only need one test to test the business logic: "given three RGB-valid colors, does this function return the correct HEX value?" — a great improvement!

我们已经找到了一个可行的解决方案。通过使用 RgbValue，我们的大多数测试变得多余。现在我们只需要一个测试来测试业务逻辑："给定三个 RGB 有效的颜色，这个函数是否返回正确的 HEX 值？"——这是一个很大的改进！

```php
function rgbToHex(RgbValue $red, RgbValue $green, RgbValue $blue) 

{
    // …
}

```

But Hold On…

但是等等……

If one of the claimed benefits of type systems is to prevent runtime bugs and errors, then we're still not getting anywhere with our RgbValue . PHP will check this type at runtime and throw a type error when the program is running. In other words: things can still go horribly wrong at runtime, maybe even in production. This is where static analysis comes in.

如果类型系统声称的好处之一是防止运行时 bug 和错误，那么我们的 RgbValue 仍然没有取得任何进展。PHP 会在运行时检查这个类型，并在程序运行时抛出类型错误。换句话说：事情仍然可能在运行时出错，甚至可能在生产环境中。这就是为什么需要静态分析。

Instead of relying on runtime type checks (and throwing errors to handle them), static analysis tools will test your code without running it. If you're using any kind of IDE, you're already making use of it. When your IDE tells you what methods are available on an object, what input a function requires, or whether you're using an unknown variable, it's all thanks to static analysis.

静态分析工具不会依赖运行时类型检查（并抛出错误来处理它们），而是在不运行代码的情况下测试你的代码。如果你使用任何类型的 IDE，你已经在使用它了。当你的 IDE 告诉你对象上可用的方法、函数需要什么输入，或者你是否使用了未知变量时，这都归功于静态分析。

Granted, runtime errors still have their merit: they stop code from further executing when a type error occurs, so they probably are preventing actual bugs. They also provide useful information to the developer about what exactly went wrong and where. But still, the program crashed. Catching the error before running code in production will always be the better solution.

当然，运行时错误仍然有其优点：当发生类型错误时，它们会阻止代码进一步执行，所以它们可能确实在防止实际的 bug。它们还为开发人员提供了关于到底出了什么问题以及在哪里出错的有用信息。但程序仍然崩溃了。在生产环境中运行代码之前捕获错误总是更好的解决方案。

Some other programming languages even go as far as to include a static analyser in their compiler: if static analysis checks fail, the program won't compile. Since PHP doesn't have a standalone compiler, we'll need to rely on external tools to help us.

一些其他编程语言甚至在其编译器中包含静态分析器：如果静态分析检查失败，程序将无法编译。由于 PHP 没有独立的编译器，我们需要依赖外部工具来帮助我们。

## PHP Compiler

Even though PHP is an interpreted language, it still has a compiler. PHP code is compiled on the fly when, for example, a request comes in. There are of course, caching mechanisms in play to optimise this process, but there's no standalone compilation phase.This allows you to easily write PHP code and immediately refresh the page without having to wait for a program to compile, one of the well-known strengths of PHP development.

尽管 PHP 是一种解释型语言，它仍然有一个编译器。PHP 代码在运行时（例如，当请求到来时）即时编译。当然，有缓存机制在起作用以优化这个过程，但没有独立的编译阶段。这允许你轻松编写 PHP 代码并立即刷新页面，而不必等待程序编译，这是 PHP 开发的众所周知优势之一。

Luckily there are great community-driven static analysers for PHP available. They are standalone tools that look at your code and all its type hints allowing you to discover errors without ever running the code. These tools will not only look at PHP's types, but also at doc blocks, meaning they allow for more flexibility than normal PHP types would.

幸运的是，有很棒的社区驱动的 PHP 静态分析器可用。它们是独立的工具，查看你的代码及其所有类型提示，允许你在不运行代码的情况下发现错误。这些工具不仅会查看 PHP 的类型，还会查看文档块，这意味着它们比普通 PHP 类型允许更多的灵活性。


Take a look at how Psalm would analyse your code and report errors:

看看 Psalm 如何分析你的代码并报告错误：
```
Analyzing files==.

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   60 / 1038 (5%)

…

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1038 / 1038 (100%)

ERROR: TooFewArguments

    …

    Too few arguments for method …\PriceCalculatorFactory=:withproduct ERROR: TooFewArguments 

    …

    Too few arguments for method …\Checkable=:ischeckable

------------------------------

2 errors found

------------------------------
```
Here we see Psalm scanning over a thousand source files and detecting where we forgot to pass the correct amount of arguments to a function. It does so by analysing method signatures and comparing them to how those methods are called. Of course, type definitions play an important role in this process.

这里我们看到 Psalm 扫描了一千多个源文件，并检测到我们忘记向函数传递正确数量的参数的地方。它通过分析方法签名并将它们与这些方法的调用方式进行比较来实现这一点。当然，类型定义在这个过程中起着重要作用。

Most static analysers even allow custom doc block annotations that support, for example, generics. By doing so they can do much more complex type checks than PHP could do at runtime. Even when running the code wouldn't perform any checks, the static analyser could tell you when something is wrong beforehand. Such static type checks could be done locally when writing code, built into your CI pipeline, or a mix of both.

大多数静态分析器甚至允许自定义文档块注释，支持例如泛型。通过这样做，它们可以执行比 PHP 在运行时能够执行的更复杂的类型检查。即使运行代码不会执行任何检查，静态分析器也可以提前告诉你什么时候出了问题。这种静态类型检查可以在编写代码时在本地完成，内置到你的 CI 管道中，或者两者兼而有之。

In fact, the static analysis community is getting so much traction these days that PhpStorm — the most popular IDE for writing PHP code — added built-in support for them. This means that the result of several type checks performed by your static analyser can be shown immediately when writing code.

事实上，静态分析社区这些天获得了如此大的关注，以至于 PhpStorm——最流行的编写 PHP 代码的 IDE——添加了对它们的内置支持。这意味着你的静态分析器执行的几种类型检查的结果可以在编写代码时立即显示。

Tools like Psalm, PHPStan, and Phan are great, but they also lack the eloquence you'd get from built-in language support. I've gone on and on about removing doc blocks in favour of built-in types in the previous chapter, and now we're adding them again to support static analysis. Now, to be clear: these tools also work with PHP's built-in type system (without using any doc blocks), but those doc block annotations offer a lot more functionality, because PHP's syntax doesn't limit them; they are comments, after all.

像 Psalm、PHPStan 和 Phan 这样的工具很棒，但它们也缺乏内置语言支持所能获得的优雅。我在前一章中反复强调用内置类型替换文档块，现在我们又添加它们来支持静态分析。现在，要明确的是：这些工具也可以与 PHP 的内置类型系统一起工作（不使用任何文档块），但那些文档块注释提供了更多功能，毕竟注释也是有用的。

On the other hand (I've said this before in the previous chapter), there's little chance that features like generics will be added anytime soon in PHP itself since they pose such a threat to runtime performance. So if there's nothing better, we'll have to settle with doc blocks anyway if we want to use static analysis to its full extent.

另一方面（我在前一章中已经说过这一点），像泛型这样的功能在 PHP 本身中很快被添加的可能性很小，因为它们对运行时性能构成如此大的威胁。所以如果没有更好的选择，如果我们想充分利用静态分析，我们无论如何都必须使用文档块。

If only… Can you see where I'm going with this?What if PHP supported the generic syntax, but didn't interpret it at runtime? What if you'd need to use a static analyser to guarantee correctness (when using generics), and wouldn't worry about them when running your code. That's exactly the point of static analysis.

如果……你能看出我要说什么吗？如果 PHP 支持泛型语法，但在运行时不解释它呢？如果你需要使用静态分析器来保证正确性（在使用泛型时），而在运行代码时不必担心它们。这正是静态分析的意义所在。

You might be afraid of PHP not enforcing those type checks at runtime. Still, you could also argue that static analysers are way more advanced in their capabilities, exactly because they aren't run when executing code. I don't think it's such a convoluted idea at all, and in fact, other languages already use this approach. Think about TypeScript, which has grown in popularity tremendously over the years. It's compiled to JavaScript, and all its type checks are done during that compilation phase, without running the code. Now I'm not saying we need another language that compiles to PHP; I'm only saying that static analysers are very powerful tools. If you decide to embrace them, you'll notice how you can reduce the number of tests and how rarely runtime type errors occur.

你可能担心 PHP 不会在运行时强制执行这些类型检查。但是，你也可以争辩说，静态分析器在其能力上要先进得多，正是因为它们不在执行代码时运行。我认为这根本不是那么复杂的想法，事实上，其他语言已经在使用这种方法。想想 TypeScript，它在过去几年中获得了巨大的流行。它被编译为 JavaScript，其所有类型检查都在该编译阶段完成，而不运行代码。现在我不是说我们需要另一种编译为 PHP 的语言；我只是说静态分析器是非常强大的工具。如果你决定接受它们，你会注意到你可以减少测试的数量，以及运行时类型错误很少发生。

Where does that leave us now? Unfortunately, not very far. I'd recommend using a static analyser in your projects, regardless of whether you want to use its advanced annotations or not. Even without those, static analysers offer a great benefit. You've got much more certainty strange edge cases aren't possible, and you need to write fewer tests, all without ever running that code once. It's a great tool to have in your toolbox, and maybe one day, we'll see PHP fully embrace its benefits.

那么我们现在处于什么阶段？不幸的是，进展不大。我建议在你的项目中使用静态分析器，无论你是否想使用其高级注释。即使没有这些，静态分析器也提供了巨大的好处。你可以更确定奇怪的边界情况是不可能的，你需要编写更少的测试，所有这些都不需要运行代码一次。这是你工具箱中的一个很好的工具，也许有一天，我们会看到 PHP 完全接受它的好处。

In action

Ready to see what static analysis can do for you? I'd recommend to go to psalm.dev and play around with their interactive playground. Some great examples show the full power of static analysis.

准备好看看静态分析能为你做什么吗？我建议访问 psalm.dev 并在他们的交互式 playground 中玩一玩。一些很好的例子展示了静态分析的完整功能。