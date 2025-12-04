# CHAPTER 06

## NAMED ARGUMENTS Just like constructor property promotion, named arguments are a new syntactical addition in PHP 8. They allow you to pass variables to a function based on the argument name in that function, instead of their position in the argument list. Here's an example with a built-in PHP function:

setcookie(

    name: 'test',

    expires: time() + 60 * 60 * 2,

    secure: true,

);And here's it used when constructing a DTO:

```php
class CustomerData

{

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}
$data = new CustomerData(

```

    age: $input['age'],

    email: $input['email'],

    name: $input['name'],

```php
);

```

Named arguments are a great new feature and will have a significant impact on my day-to-day programming life. You're probably wondering about the details. What if you pass a wrong name, or what about combining ordered and named arguments? 

Well, let's look at all those questions in-depth.

Why named arguments?

This feature was a highly debated one. There were some concerns about adding them, especially with regards to backwards compatibility. If you're maintaining a package and decide to change an argument's name, this now counts as a breaking change. Take for example this method signature, provided by a package:

```php
public function toMediaCollection(

```

    string $collection, 

    string $disk = null

```php
): void { /* … */ }

```

If the users of this package would use named arguments, they write something like this:

```php
$media=>toMediaCollection(

```

    collection: 'default',

    disk: 'aws',

```php
);

```

Now imagine you, the package maintainer, want to change the name of $collection to $collectionName . This means the code written by your users would break.

I agree this is a problem in theory, but being an open source maintainer myself, I know from experience that such variable name changes very rarely occur. The only times I can remember that we did such a change was because we were working on a new major release anyway, where breaking changes are allowed.

While I recognise the theoretical problem, I firmly believe this is a non-issue in prac -

tice. Such name changes rarely happen. And even if you really wouldn't want to be bothered with managing variable names as an open source maintainer, you could still add a warning in your package's README file. It could tell your users that variable names might change, and they should use named arguments at their own risk. I prefer just to keep it in mind, and remember that I should be careful changing variable names in the future. No big deal.Despite this minor inconvenience, I'd say the benefits of named arguments are far more significant. The way I see it: named arguments will allow us to write cleaner and more flexible code.

For one, named arguments allow us to skip default values. Take a look again at the cookie example:

setcookie(

    name: 'test',

    expires: time() + 60 * 60 * 2,

    secure: true,

```php
);

```

Its method signature is actually the following:

setcookie( 

    string $name, 

    string $value = '', 

    int $expires = 0, 

    string $path = '', 

    string $domain = '', 

    bool $secure = false, 

    bool $httponly = false,

) : bool In the example with named arguments, we didn't need to set a cookie $value , but we did need to set an expiration time. Named arguments made this method call a little more concise, because otherwise it would have looked like this:

setcookie(

    'test',

    '',

    time() + 60 * 60 * 2,

    '',

    '',

    true

```php
);

```

Besides skipping arguments with default values, there's also the benefit of clarifying which variable does what, something that's especially useful in functions with large method signatures. We could say that lots of arguments are usually a code smell; we still have to deal with them no matter what. So it's better to have a good way of doing so than nothing at all.

Named Arguments in Depth Let's look at what named arguments can and cannot do with the basics out of the way.First of all, they can be combined with unnamed — also called ordered — arguments. 

In that case, the ordered arguments must always come first. Take our DTO example from before:

```php
class CustomerData

{

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}

```

You could construct it like so:

```php
$data = new CustomerData(
$input['name'],

```

    age: $input['age'],

    email: $input['email'],

```php
);

```

However, having an ordered argument after a named one would throw an error:

```php
$data = new CustomerData(

```

    age: $input['age'],

```php
$input['name'],

```

    email: $input['email'],

```php
);

```

Next, it's possible to use array spreading in combination with named arguments:

```php
$input = [

```

    'age' => 25,

    'name' => 'Brent',

    'email' => 'brent@spatie.be',

```php
];
$data = new CustomerData(==.$input);

```

Heads up!

Just like with variadic functions, arrays can be spread using the ==. operator. 

We'll take all arguments from the input array and spread them into a function. If the array contains keyed values, those key names will map onto named proper -

ties as well, and that is what's happening in the above example.

If, however, there are missing required entries in the array, or if there's a key not listed as a named argument, an error will be thrown:

```php
$input = [

```

    'age' => 25,

    'name' => 'Brent',

    'email' => 'brent@spatie.be',

    'unknownProperty' => 'This is not allowed',

```php
];
$data = new CustomerData(==.$input);It is possible to combine named and ordered arguments in an input array, but only if the ordered arguments follow the same rule as before: they must come first!
$input = [

```

    'Brent',

    'age' => 25,

    'email' => 'brent@spatie.be',

```php
];
$data = new CustomerData(==.$input);

```

Be careful mixing ordered and named arguments though. I personally don't think they improve readability at all.

Variadic Functions If you're using variadic functions, named arguments will be passed with their key name into the variadic arguments array. Take the following example:

```php
class CustomerData

{

    public static function new(==.$args): self

    {

        return new self(==.$args);

    }

    public function =_construct(

        public string $name,

        public string $email,

        public int $age,

    ) {}

}
$data = CustomerData=:new(

```

    email: 'brent@spatie.be',

    age: 25,

    name: 'Brent',

```php
);

```

// [

//     'age' => 25,

//     'email' => 'brent@spatie.be',

//     'name' => 'Brent',

// ]Here we are again with the mysterious attributes feature - we'll cover them in depth soon! For now, I can tell you that they also support named arguments when construct -

ing them:

```php
class ProductSubscriber

{

```

    =[ListensTo(event: ProductCreated=:class)]

```php
    public function onProductCreated(ProductCreated $event) { /* … */ }

}

```

Other Things Worth Noting It's not possible to have a variable as the argument name:

```php
$field = 'age';
$data = CustomerData=:new(
$field: 25,

);

```

And finally, named arguments will deal in a pragmatic way with name changes during inheritance. Take this example:

```php
interface EventListener {

    public function on($event, $handler);

}

class MyListener implements EventListener

{

    public function on($myEvent, $myHandler)

    {

```

        // …

```php
    }

}

```

PHP will silently allow changing the name of $event  to $myEvent , and $handler  to 

```php
$myHandler ; but  if you decide to use named arguments using the parent's name, it will result in a runtime error:

public function register(EventListener $listener)

{
$listener=>on(

```

        event: $this=>event,

        handler: $this=>handler, 

```php
    );

}

```

This pragmatic approach was chosen to prevent a major breaking change where all inherited arguments would have to keep the same name. It seems like an excellent solution to me. You can expect to see named arguments used in this book here and there. I think they are great syntactical sugar.
