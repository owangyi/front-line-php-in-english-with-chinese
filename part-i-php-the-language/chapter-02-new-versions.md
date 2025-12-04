# CHAPTER 02

## NEW VERSIONS

Since this book aims to bring you up to speed with modern PHP practices, it's important to know what happened to the language over the past decade or so. With the development and release of PHP 7, the PHP landscape changed dramatically. I like to think of the PHP 7.x versions as a maturity phase for the language, so this is where we will start.

First and foremost, PHP 7.0 comes with a significant performance boost. Much of PHP's core was rewritten, which resulted in a noticeable difference. It's not uncommon to see your application run two or three times as fast, just by using PHP 7 or higher. 

Thanks to one of PHP's core values — maintaining backwards compatibility — old PHP 5 codebases can easily be updated to benefit from these changes.

What happened to 6?

PHP 5.6 was the latest version in the 5 series, with the next one being 7.0. What happened to version 6? The core team started working on it, only to realise rather late that there were major issues with the internal implementation. 

They decided to rework the engine once again, but "PHP 6" was already being written. To avoid confusion, they decided to skip version 6, and jump straight to PHP 7.

The story of PHP 6 has become folklore within the community. If you want to know the in-depth story, you can do a quick Google search.Even though PHP 7.0 was such a milestone, we've since moved on from it as well. 

PHP 7.0 is already considered old: it was released in 2015 and didn't receive updates anymore five years later. Around the late 5.x releases, PHP adopted a strict release cycle: every year brings one new version. Most versions are actively supported for two years, followed by one year of additional security support. After three years, you should update, as the version you are using doesn't get security patches anymore.

Arguably, it's even better to follow along with the latest version. There will always be minor breaking changes and deprecations, but most code can easily be updated. 

There even are great automated tools that will take your existing codebase, detect any upgrading errors, and fix them automatically.

Automation One of those automated tools is called Rector which has grown in popularity over the years: https://github.com/rectorphp/rector . Rector can update your codebase automatically across several PHP versions and is a great tool to know about if you ever have to deal with legacy projects.

In the next few chapters, we'll take a deep dive into the features added in PHP 7 and PHP 8. Before doing that, we'll start by looking at the smaller yet significant changes in this chapter.

Trailing commas Support for trailing commas has been added incrementally up until PHP 8.0. They are now supported in arrays, function calls, parameter lists, and closure use statements.

Trailing commas are a somewhat controversial topic among developers. Some people like them; others hate them. One argument in favour of trailing commas is that they make diffs easier. For example, imagine an array with two elements:

```php
$array = [
$foo,
$bar

];

```

Next you'd need to add a third:

```php
$array = [
$foo,
$bar,
$baz

```

];Version control systems such as GIT would list two changes instead of one, because you really did make two actual changes. If you'd always used trailing commas, you wouldn't need to alter the existing lines:

```php
$array = [
$foo,
$bar,
$baz,

];

```

Besides version control diffs, trailing commas can also be considered "easier" to reason about because you never have to worry about adding an extra comma or not. 

You might not prefer this writing style, and that's fine. We'll discuss the importance of a style guide in a later chapter.

Formatting numeric values You can use an underscore to format numeric values. This underscore is completely ignored when the code is parsed but makes long numbers easier to read by humans.

This can be especially useful in tests. Take the following example: we're testing an invoice flow and we need to pass in an amount of money. It's a good idea to store money in cents, to prevent rounding errors, so using an _ makes it clearer:

```php
public function test_create_invoice()

{

```

    // $100 and 10 cents

```php
$invoice = new Invoice(100_10);

    

```

    // Assertions

```php
}

```

Anonymous classes Anonymous classes were added in PHP 7.0. They can be used to create objects on the fly; they can even extend a base class. Here's an example in a test context:

```php
public function test_dto_type_checking_with_arrays(): void

{
$dto = new class(

```

        ['arrayOfInts' => [1, 2]]

```php
    ) extends DataTransferObject {

```

        /** @var int[] */

```php
        public array $arrayOfInts;

    }; 

```

    // Assertions

}Flexible heredoc Heredoc can be a useful tool for larger strings, though they had an annoying indenta -

tion quirk in the past: you couldn't have any whitespaces in front of the closing delim -

iter. In effect, that meant you had to do this:

```php
public function report(): void

{
$query = ==<SQL SELECT * 

```

        FROM `table`

```php
        WHERE `column` = true;

SQL;

    

```

    // …

```php
}

```

Fortunately, you can now do this:

```php
public function report(): void

{
$query = ==<SQL SELECT * 

```

        FROM `table`

```php
        WHERE `column` = true;

    SQL;

    

```

    // …

```php
}

```

The whitespace in front of the closing marker will be ignored on all lines.

Exception improvements Let's take a look at two smaller additions in PHP 8. First: a throw statement is now an expression. That means you can use it in more places, such as the null coalescing righthand operand, or in short closures; we'll cover both of those features in-depth later.

// Invalid before PHP 8

```php
$name = $input['name'] =? throw new NameNotFound();

```

// Valid as of PHP 8

```php
$name = $input['name'] =? throw new NameNotFound();
$error = fn (string $class) => throw new $class(); 

```

Second: exceptions support non-capturing catches. There might be cases where you want to catch an exception to keep the program flow going and not do anything with it. You always had to assign a variable to the caught exception, even when you didn't use it. That's not necessary anymore:

```php
try {

```

    // Something goes wrong

```php
} catch (Exception) {

```

    // Just continue

}Weak references and maps PHP 7.4 added the concept of weak references. To understand what they are, you need to know a little bit about garbage collection. Whenever an object is created, it requires some memory to keep track of its state. If an object is created and assigned to a variable, then that variable is a reference to the object. As soon as there are no references to an object anymore, it cannot be used, and it doesn't make sense to keep it in memory. That's why the garbage collector sometimes comes along looking for those kinds of objects and removes them, freeing memory.

Weak references are references to objects which don't prevent them from being garbage collected. This feature on its own might seem a little strange, but they allow an interesting use case as of PHP 8, combined with weak maps: a map of objects which are referenced using weak references.

Take the example of ORMs: they often implement caches which hold references to entity classes to improve the performance of relations between entities. These entity objects can not be garbage collected, as long as this cache has a reference to them, 

even if the cache is the only thing referencing them.

If this caching layer uses weak references and maps instead, PHP will garbage collect these objects when nothing else references them anymore. Especially in the case of ORMs, which can manage several hundred, if not thousands of entities within a request; weak maps can offer a better, more resource-friendly way of dealing with these objects.

Here's what weak maps look like:

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

In this example, we cache the result of an expensive operation related to an object in a cache. If the result doesn't exist yet, we'll compute it once. Thanks to weak maps, this object can still be garbage collected if there are no other references to it anymore.The JIT — just in time — compiler is a core mechanism added in PHP 8 which can significantly speed up PHP code.

A JIT compiler will look at code while running and tries to find pieces of that code that are executed often. The compiler will take those parts and compile them to machine code — on the fly — and use the optimised machine code from then on out. The technique can be used in interpreted languages like JavaScript, and now also in PHP. It has the potential to improve an application's performance significantly.

I say "potential" because there are a few caveats we must take into account. I'll keep those and everything else JIT-related for the chapter dedicated to the JIT.

Class shorthand on objects The =:class  shorthand was added in PHP 5.5 to quickly get the full class name of an imported one:

```php
$className = Offer=:class;

```

In PHP 8 this also works with variables:

```php
$className = $offer=:class;

```

Improved string to number comparisons One of PHP's dynamic type system strengths is one of its weaknesses at the same time: type juggling. PHP will try to change a variable's type when it encounters a strange piece of code. Here's an example where strings and numbers are compared:

'1' == 1 // true If you don't want this type juggling, you'd use the triple === sign instead:

'1' === 1 // false There are strange edge cases when using weak comparisons, though. The following returns true in versions before PHP 8:

'foo' == 1 // true As of PHP 8, this behaviour is improved. The example above, as well as other edge cases, would now return false correctly.

'foo' == 1 // falseChanges to the error control operator One last notable change is that the @ operator no longer silences fatal errors. You can still use it to silence other kinds of errors, like so:

```php
$file = @file_get_contents('none/existing/path');

```

In cases where you don't use the @ operator, an error would be triggered, but with @, 

```php
$file  will simply be false. If, on the other hand, a fatal error is thrown in PHP 8, the @ 

```

operator wouldn't ignore it anymore.

Deep down in the core There are two low-level components added to PHP's core with the 7.4 update: FFI and preloading. These are two complex topics on their own, each with their own chapter. 

I'll briefly mention them here, though.

FFI — a.k.a. foreign function interface — allows PHP to speak to shared libraries written in, for example C, directly. To put that in other words: it's possible to write PHP extensions and ship them as composer packages without installing the low-level PHP extensions themselves. I promise we'll dive deeper into this soon!

The other one — preloading — enables you to compile PHP code on server startup. 

That code will be kept in memory for all subsequent requests. It can speed up your average PHP web framework since it doesn't have to boot anymore on every request. 

Again: this one deserves a chapter on its own.

So with these random little features out of the way, let's dig deeper into all great things added to PHP over the past years!
