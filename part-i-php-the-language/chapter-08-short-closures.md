# CHAPTER 08

## SHORT CLOSURES Some might consider them long overdue, but they are finally supported since PHP 7.4: 

short closures. Instead of writing closures like the one passed as an array_map  callback:

```php
$itemPrices = array_map(

    function (OrderLine $orderLine) {

        return $orderLine=>item=>price;

```

    }, 

```php
$order=>lines

);

```

You can write them in a short form:

```php
$itemPrices = array_map(

```

    fn ($orderLine) => $orderLine=>item=>price,

```php
$order=>lines

);

```

Short closures differ from normal closures in two ways:

• they only support one expression, and that's also the return statement; and

• they don't need a use statement to access variables from the outer scope.Concerning everything else, they act like a normal closure would: they support refer -

ences, argument spreading, type hints, return types… Speaking of types, you could rewrite the previous example in more strictly typed way, like so:

```php
$itemPrices = array_map(

```

    fn (OrderLine $orderLine): int => $orderLine=>item=>price,

```php
$order=>lines

);

```

One more thing, references are also allowed, both for the arguments as well as the return values. If you want to return a value by reference, the following syntax should be used:

fn&($x) => $x No Mul ti-Line You might have noticed it already: short closures can only have one expression; it may be spread over multiple lines for formatting, but it must always be one expression. The reasoning is as follows: the goal of short closures is to reduce verbosity. fn is of course shorter than function  in all cases. However, it was argued that if you're dealing with multi-line functions, there is less to be gained by using short closures. 

After all, multi-line closures are by definition already more verbose; so being able to skip two keywords ( function  and return ) wouldn't make much of a difference.

While I can think of many one-line closures in my projects, there are also plenty of multi-line ones, and I admit to missing the short syntax in those cases. There's hope, 

though: it will be possible to add multi-line short closures in the future, but we'll have to wait still a little longer.

Values from Outer Scope Another significant difference between short and normal closures is that the short ones don't require the use keyword to be able to access data from the outer scope:

```php
$modifier = 5;

array_map(fn ($x) => $x * $modifier, $numbers);

```

It's important to note that you won't be able to modify variables from that outer scope: 

they are bound by value and not by reference, that is unless you're dealing with objects that are always passed by reference. That's the default behaviour for objects everywhere, by the way, not just in short closures.

One exception is of course the $this  keyword, which acts exactly the same as normal closures:

```php
array_map(fn ($x) => $x * $this=>modifier, $numbers);

```

Speaking of $this , you can declare a short closure to be static , which means you won't be able to access $this  from within it:

```php
static fn ($x) => $x * $this=>modifier;

```

// Fatal error: Uncaught Error: Using $this when not in object context That's about all there is to say about short closures for now. You can imagine there's room for improvement. People have been talking about multi-line short closures and being able to use the syntax for class methods. We'll have to wait for future versions to see whether and how short closures will evolve.
