# CHAPTER 09

## WORKING WITH ARRAYS I've already used some array-specific syntax in the previous chapters, so it seems like a good idea to dedicate some time to them as well. Now don't worry: I won't discuss all array-related functions in PHP, there are too many of them, which would be rather boring. No, I'll only talk about what's made possible with arrays and PHP's syntax over the last year. There have been quite a lot of niceties added when dealing with arrays. 

We'll talk all about it in this chapter.

Rest and Spread You've already seen the two uses of the ==. operator in previous examples: you can use it to "spread" array elements and pass them individually to functions, as well as make variadic functions that collect the "rest" of the arguments into an array.

Let's quickly recap. Here we're spreading array elements into a function:

```php
$data = ['a', 'b', 'c'];

function handle($a, $b, $c): void { /* … */ }

```

handle(==.$data);And here, we're using a variadic function, which collects the remaining parameters and stores them in an array.

```php
function handle($firstInput, ==.$listOfOthers) { /* … */ }

handle('a', 'b', 'c', 'd');

```

In this case, $firstInput  will be 'a', while $listOfOthers  will be an array: 

['b', 'c', 'd'] .

One interesting thing about variadic functions is that you can type hint them as well, 

so you can say that all variables passed into $listOfOthers  should be, for example, 

strings:

```php
function handle($firstInput, string ==.$listOfOthers) { /* … */ }

```

You could also combine the two together. Here's a generic implementation of a static constructor for any class. It's wrapped in a trait so that it can be used in whatever class you want.

```php
trait Makeable

{

    public static function make(==.$args): static

    {

        return new static(==.$args);

    }

}

```

In this example, we're taking a variable amount of input arguments and spreading them again into the constructor. This means that, whatever amount of variables the constructor takes, we can use make  to pass those variables to it. Here's what that would look like in practice:

```php
class CustomerData

{  

    use Makeable;

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}
$customerData = CustomerData=:make($name, $email, $age);

```

// Or you could use array spreading again:

```php
$customerData = CustomerData=:make(==.$inputData);

```

One more thing to mention about array spreading: the syntax can be used to combine arrays as well:

```php
$inputA = ['a', 'b', 'c'];
$inputB = ['d', 'e', 'f'];
$combinedArray = [==.$inputA, ==.$inputB];

```

// ['a', 'b', 'c', 'd', 'e', 'f']It's a shorthand way to merge two arrays. There's one important note, though: you're only allowed to use this array-in-array-spreading syntax when the input arrays only have numeric keys - textual keys aren't allowed.

Array Destructuring Array destructuring is the act of pulling elements out of an array — it's about "de -

structuring" an array into separate variables. You can use both list  or [] to do so. 

Note that the word is "destructure", not "destruction"!

Here's what that looks like:

```php
$array = [1, 2, 3]; 

```

// Using the list syntax:

```php
list($a, $b, $c) = $array;

```

// Or the shorthand syntax:

```php
[$a, $b, $c] = $array;

```

// $a = 1

// $b = 2

// $c = 3 Whether you prefer list  or its shorthand [] is up to you. People might argue that [] 

is ambiguous with the shorthand array syntax and thus prefer list. I'll be using the shorthand version in code samples as that is my preference. I think that since the [] 

notation is on the left side of the assignment operator, it's clear enough that it's not an array definition.

So let's look at what's possible using this syntax.

Skipping Elements Say you only need the third element of an array; the first two can be skipped by simply not providing a variable.

```php
[, , $c] = $array;

```

// $c = 3 Also note that array destructuring on arrays with numeric indices will always start at index 0. Take for example the following array:

```php
$array = [

```

    1 => 'a',

    2 => 'b',

    3 => 'c',

```php
];

```

The first variable pulled out would be null , because there's no element with index 0. 

This might seem like a shortcoming, but luckily there are more possibilities.Non-Numerical Keys PHP 7.1 allows array destructuring to be used with arrays that have non-numerical keys. This allows for more flexibility:

```php
$array = [

```

    'a' => 1,

    'b' => 2,

    'c' => 3,

```php
];

['c' => $c, 'a' => $a] = $array;

```

As you can see, you can change the order however you want, and also skip elements entirely.

In Practice One of the uses of array destructuring are with functions like parse_url  and pathinfo . 

Because these functions return an array with named parameters, we can destructure the result to pull out the information we'd like:

[

    'basename' => $file,

    'dirname' => $directory,

```php
] = pathinfo('/users/test/file.png');

```

You can also see in this example that the variables don't need the same name as the key. If you're destructuring an array with an unknown key however, PHP will issue a notice:

[

    'path' => $path, 

    'query' => $query,

```php
] = parse_url('https:=/front-line-php.com');

```

// PHP Notice:  Undefined index: query In this case, $query  would be null . You could observe one last detail in the example: 

trailing commas are allowed with named destructs, just like you're used to with arrays.In Loops Array destructuring has even more use cases — you've already seen this one used in the attributes chapter. You can destructure arrays in loops:

```php
$array = [

```

    [

        'name' => 'a',

        'id' => 1

    ],

    [

        'name' => 'b',

        'id' => 2

    ],

```php
];

foreach ($array as ['id' => $id, 'name' => $name]) {

```

    // …

```php
}

```

This could be useful when parsing, for example, a JSON or CSV file. Only be careful that undefined keys will still trigger a notice.

So there we have it: you're up to date with everything you can do using arrays in modern-day PHP. I find that most of these syntactical additions have their use cases. 

There are always other ways to achieve the same result that don't rely on shorthands 

- it's your choice. We'll talk more about these kinds of preferences in the chapter on style guides, but there are a few other topics to discuss first.
