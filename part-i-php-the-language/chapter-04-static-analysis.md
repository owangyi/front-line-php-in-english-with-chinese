# CHAPTER 04

## STATIC ANALYSIS Static Anal ysis Having spent a whole chapter on PHP's type system, I realise I haven't discussed why you want to use it. I realise a significant part of the community doesn't like using PHP's type system, so it's important to discuss both the pros and cons thoroughly. 

That's what we'll do in this chapter. We'll start by discussing the value provided by a type system.

Many think of programming languages with a stricter type system to have fewer or no runtime errors. There's the popular saying that a strong type system prevents bugs, 

but that's not entirely true. You can easily write bugs in a strongly typed language, but a range of bugs is not possible anymore since a good type system prevents them.

Are you unsure what the difference is between strong, weak, static and dynamic type systems? We'll cover the topic in-depth later in this chapter!

Imagine a simple function: rgbToHex . It takes three arguments, each of which are in -

tegers between 0 and 255. The function then converts the integers to a hexadecimal string. Here's what this function's definition might look like without using types:

```php
function rgbToHex($red, $green, $blue) {

```

    // …

}Since we want to ensure our implementation of this function is correct, we write tests:

```php
assert(rgbToHex(0, 0, 0) === '000000');

assert(rgbToHex(255, 255, 255) === 'ffffff');

assert(rgbToHex(238, 66, 244) === 'ee42f4');

```

These tests ensure that everything works as expected. Right?

Well… we're only testing three out of the 16,777,216 possible RGB combinations. But logic reasoning tells us that if these three sample cases work, we're probably safe. 

What happens though if we pass floats instead of integers?

```php
rgbToHex(1.5, 20.2, 100.1);

```

Or numbers outside of the allowed range?

```php
rgbToHex(-504, 305, -59);

```

What about null ?

```php
rgbToHex(null, null, null);

```

Or strings?

```php
rgbToHex('red', 'green', 'blue');

```

Or the wrong number of arguments?

```php
rgbToHex();

rgbToHex(1, 2);

rgbToHex(1, 2, 3, 4);

```

Or a combination of the above?

I can easily think of five edge-cases we need to test before there's relative certainty that our program does what it needs to do. That's at least eight tests we need to write, and I'm sure you can come up with a few others. These are the kinds of prob -

lems a type system aims to partially solve, and note the word partially because we'll come back to it. If we filter the input by a specific type, many of our tests become obsolete. Say we'd only allow integers:

```php
function rgbToHex(int $red, int $green, int $blue) 

{

```

    // …

```php
}

```

You can think of types as a subcategory of all available input; it's a filter that only allows specific items.

Let's take a look at the tests that aren't necessary anymore thanks to our int type hint:

• Whether the input is numeric

• Whether the input is a whole number

• Whether the input isn't nullWe still need to check whether the input number is between 0 and 255. At this point, 

we run against the limitations of many type systems, including PHP's. Sure we can use int, though in many cases, the category described by this type is still too large for our business logic: int would also allow -100  to be passed, which wouldn't make any sense for our function. Some languages have a uint  or "unsigned integer" type; yet it is also too large a subset of "numeric data".

Luckily, there are ways to address this issue.

One approach could be to use "configurable" or generic types, for example int<min, max> . The concept of generics is known in many programming languages, 

though unfortunately not in PHP. In theory, a type could be preconfigured so that it is smart enough to know about all your business logic.

Languages like PHP lack the flexibility of generic types, but we do have classes, which can be used as types themselves. We could, for example, represent a configurable 

"integer" with a class IntWithinRange :

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

    

```

    // …

```php
}

```

So whenever we're using an instance of IntWithinRange , we can ensure its value is constrained within a subset of integers. But this only works when constructing IntWithinRange . In practice, we can't ensure its minimum and maximum value in our rgbToHex  function, meaning we can't say we only accept IntWithinRange  object witha minimum of 0 and a maximum of 255. Therefore we can only say we accept any object with the type of IntWithinRange :

```php
function rgbToHex(

```

    IntWithinRange $red, 

    IntWithinRange $green, 

    IntWithinRange $blue

```php
) {

```

    // …

```php
}

```

To solve this, we need an even more specific type: RgbValue :

```php
class RgbValue extends IntWithinRange

{

    public function =_construct(int $value) 

    {

        parent=:=_construct(0, 255, $value);

    }

}

```

We've arrived at a working solution. By using RgbValue , most of our tests become redundant. We now only need one test to test the business logic: "given three RGB-valid colors, does this function return the correct HEX value?" — a great improvement!

```php
function rgbToHex(RgbValue $red, RgbValue $green, RgbValue $blue) 

{

```

    // …

```php
}

```

But Hold On…

If one of the claimed benefits of type systems is to prevent runtime bugs and errors, 

then we're still not getting anywhere with our RgbValue . PHP will check this type at runtime and throw a type error when the program is running. In other words: things can still go horribly wrong at runtime, maybe even in production. This is where static analysis comes in.

Instead of relying on runtime type checks (and throwing errors to handle them), static analysis tools will test your code without running it. If you're using any kind of IDE, 

you're already making use of it. When your IDE tells you what methods are available on an object, what input a function requires, or whether you're using an unknown variable, it's all thanks to static analysis.

Granted, runtime errors still have their merit: they stop code from further executing when a type error occurs, so they probably are preventing actual bugs. They also provide useful information to the developer about what exactly went wrong and where. But still, the program crashed. Catching the error before running code in production will always be the better solution.

Some other programming languages even go as far as to include a static analyser in their compiler: if static analysis checks fail, the program won't compile. Since PHP doesn't have a standalone compiler, we'll need to rely on external tools to help us.

PHP Compiler Even though PHP is an interpreted language, it still has a compiler. PHP code is compiled on the fly when, for example, a request comes in. There are of course, 

caching mechanisms in play to optimise this process, but there's no standalone compilation phase.This allows you to easily write PHP code and immediately refresh the page without having to wait for a program to compile, one of the well-known strengths of PHP development.

Luckily there are great community-driven static analysers for PHP available. They are standalone tools that look at your code and all its type hints allowing you to discover errors without ever running the code. These tools will not only look at PHP's types, 

but also at doc blocks, meaning they allow for more flexibility than normal PHP types would.

Take a look at how Psalm would analyse your code and report errors:

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

Here we see Psalm scanning over a thousand source files and detecting where we forgot to pass the correct amount of arguments to a function. It does so by analysing method signatures and comparing them to how those methods are called. Of course, 

type definitions play an important role in this process.

Most static analysers even allow custom doc block annotations that support, for example, generics. By doing so they can do much more complex type checks than PHP could do at runtime. Even when running the code wouldn't perform any checks, 

the static analyser could tell you when something is wrong beforehand. Such static type checks could be done locally when writing code, built into your CI pipeline, or a mix of both.

In fact, the static analysis community is getting so much traction these days that PhpStorm — the most popular IDE for writing PHP code — added built-in support for them. This means that the result of several type checks performed by your static analyser can be shown immediately when writing code.

Tools like Psalm, PHPStan, and Phan are great, but they also lack the eloquence you'd get from built-in language support. I've gone on and on about removing doc blocks in favour of built-in types in the previous chapter, and now we're adding them again to support static analysis. Now, to be clear: these tools also work with PHP's built-in type system (without using any doc blocks), but those doc block annotations offer a lot more functionality, because PHP's syntax doesn't limit them; they are comments, after all.

On the other hand (I've said this before in the previous chapter), there's little chance that features like generics will be added anytime soon in PHP itself since they pose such a threat to runtime performance. So if there's nothing better, we'll have to settle with doc blocks anyway if we want to use static analysis to its full extent.

If only… Can you see where I'm going with this?What if PHP supported the generic syntax, but didn't interpret it at runtime? What if you'd need to use a static analyser to guarantee correctness (when using generics), 

and wouldn't worry about them when running your code. That's exactly the point of static analysis.

You might be afraid of PHP not enforcing those type checks at runtime. Still, you could also argue that static analysers are way more advanced in their capabilities, exactly because they aren't run when executing code. I don't think it's such a convoluted idea at all, and in fact, other languages already use this approach. Think about TypeScript, 

which has grown in popularity tremendously over the years. It's compiled to JavaScript, and all its type checks are done during that compilation phase, without running the code. Now I'm not saying we need another language that compiles to PHP; I'm only saying that static analysers are very powerful tools. If you decide to embrace them, you'll notice how you can reduce the number of tests and how rarely runtime type errors occur.

Where does that leave us now? Unfortunately, not very far. I'd recommend using a static analyser in your projects, regardless of whether you want to use its advanced annotations or not. Even without those, static analysers offer a great benefit. You've got much more certainty strange edge cases aren't possible, and you need to write fewer tests, all without ever running that code once. It's a great tool to have in your toolbox, and maybe one day, we'll see PHP fully embrace its benefits.

In action Ready to see what static analysis can do for you? I'd recommend to go to psalm.

dev and play around with their interactive playground. Some great examples show the full power of static analysis.
