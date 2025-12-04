# CHAPTER 05

## PROPERTY PROMOTION Having spent two chapters on the topic of PHP's type system, it's time to look at some other features in-depth. In this chapter, we'll look at an addition to PHP's syntax that gets rid of much unnecessary boilerplate code.

You might have noticed I prefer to use value objects and data transfer objects whenever possible. I like to work with simple objects only containing data and pass them around to be used within complex processes. In a later chapter, I'll share more on thisview of object-oriented code. These kinds of data-focussed objects come with lots of boilerplate code, though. Here's an example of a customer data transfer object:

```php
class CustomerDTO

{

    public string $name;

    public string $email;

    public DateTimeImmutable $birth_date;

    public function =_construct(

```

        string $name, 

        string $email, 

        DateTimeImmutable $birth_date

```php
    ) {
$this=>name = $name;
$this=>email = $email;
$this=>birth_date = $birth_date;

    }

}

```

In traditional PHP before PHP 8, you'd need to write each property's name four times. 

Thanks to constructor property promotion, you can rewrite the above like this:

```php
class CustomerDTO

{

    public function =_construct(

        public string $name, 

        public string $email, 

        public DateTimeImmutable $birth_date,

    ) {}

}

```

That's quite a difference! Let's look at this feature in-depth.

How It Works The basic idea is simple: ditch the class properties and the variable assignments, and prefix constructor parameters with public, protected or private. PHP will take that new syntax, and transform it to normal syntax under the hood, before executing the code.So when you write this code:

```php
class Person

{

    public function =_construct(

        public string $name = 'Brent',

    ) {

```

        // …

```php
    }

}

```

PHP will transform it under the hood to this:

```php
class Person

{

    public string $name;

    public function =_construct(

```

        string $name = 'Brent'

```php
    ) {
$this=>name = $name;

        

```

        // …

```php
    }

}

```

And only executes it afterwards.

This code transformation is probably known under a more common name, at least if you're somewhat familiar with the JavaScript community: transpiling. That's right: PHP will transpile itself at runtime (and cache the results for better performance). That's an interesting thought, given the previous chapter on static analysis and how I shared the language's vision adding features that are only used during static analysis.

Let's look further at what you can and cannot do with promoted properties.

Onl y in Constructors Promoted properties can only be used in constructors. That might seem obvious, but I thought it was worth mentioning, just to be clear.

Combining promoted and normal properties Not all constructor properties must be promoted - you can also mix and match:

```php
class MyClass

{

    public string $b;

    public function =_construct(

        public string $a,

```

        string $b,

```php
    ) {
$this=>b = $b;

    }

}

```

Be careful mixing the syntaxes because it can make your code less clear. Consider using a normal constructor if you're mixing promoted and non-promoted properties.No Duplicates You're not able to declare a class property and a promoted property with the same name. That's rather logical since the promoted property is transpiled to a class property at runtime:

```php
class MyClass

{

    public string $a;

    public function =_construct(

        public string $a,

    ) {}

}

```

Untyped Properties You're allowed to promote untyped properties, though as I've argued in the previous chapters, you're better off using types wherever possible:

```php
class MyDTO

{

    public function =_construct(

        public $untyped,

    ) {}

}

```

Simple Defaul ts Promoted properties can have default values, but expressions like new …  are not allowed:

```php
public function =_construct(

    public string $name = 'Brent',

    public DateTimeImmutable $date = new DateTimeImmutable(),

) {}

```

This makes sense since you're also not able to have such complex defaults with normal class properties.

Within the Constructor Body You're allowed to read the promoted properties in the constructor body. This can be useful if you want to do extra validation checks. You can use the local variable and the instance variable as both work fine:

```php
public function =_construct(

    public int $a,

    public int $b,

) {

    assert($this=>a == 100);

    if ($b == 0) {

        throw new InvalidArgumentException('…');

    }

```

}Doc Blocks You can add doc blocks to promoted properties:

```php
class MyClass 

{

    public function =_construct(

```

        /** @var string */

```php
        public $a,

    ) {}

}
$property = new ReflectionProperty(MyClass=:class, 'a');
$property=>getDocComment(); // "/** @var string */"

```

Attributes are the topic of an upcoming chapter, so consider this a sneak-peek: they are allowed on promoted properties. When transpiled, they will be present both on the constructor parameter, as well as the class property:

```php
class MyClass

{

    public function =_construct(

```

        =[MyAttribute]

```php
        public $a,  

    ) {}

}

```

Will be transpiled to:

```php
class MyClass 

{

```

    #[MyAttribute]

```php
    public $a;

 

    public function =_construct(

```

        =[MyAttribute] $a,

```php
    ) {
$this=>a = $a;

    }

}

```

Not Allowed in Abstract Constructors I must admit I didn't know abstract constructors were a thing, and I've never used them. Moreover, promoted properties are not allowed in them:

abstract class A

```php
{

```

    abstract public function =_construct(

```php
        public string $a,

    ) {}

```

}Allowed in Traits Promoted properties are  allowed in traits. It makes sense to support promoted proper -

ties in traits since the transpiled code would result in a valid trait. Whether it's a good thing or not to have constructors in traits is another question.

```php
trait MyTrait

{

    public function =_construct(

        public string $a,

    ) {}

}

```

Var is Not Supported Old - I mean, experienced PHP developers - might have used var in the distant past to declare class variables but it's not allowed with constructor promotion. Only public , 

```php
protected  and private  are valid keywords.

public function =_construct(

```

    var string $a,

```php
) {}

```

Variadic Parameters Cannot Be Promoted Since you can't convert to a type that's array of type , it's not possible to promote variadic parameters.

```php
public function =_construct(

    public string ==.$a,

) {}

```

Did you know Variadic functions make use of the rest operator ==., a feature added in PHP 5.6. It allows you to define a function input variable which will take all the "rest" 

of the variables and combine them into an array. In other words: a shorthand for func_get_args() . We'll cover variadic functions in chapter 9.

Reflection For isPromoted Both ReflectionProperty  and ReflectionParameter  have a new isPromoted()  

method to check whether the class property or method parameter is promoted.Inheritance Since PHP constructors don't need to follow their parent constructor's declaration, 

there's little to be said: inheritance is allowed. If you need to pass properties from the child constructor to the parent constructor, you'll need to pass them manually:

```php
class A

{

    public function =_construct(

        public $a,

    ) {}

}

class B extends A

{

    public function =_construct(
$a,

        public $b,    

    ) {

        parent=:=_construct($a);

    }

}

```

That's about all there is to say about property promotion. I was hesitant to use them at first, but once I gave it a try, I quickly got used to them. I must admit: promoted properties are probably my favourite feature of PHP 8.
