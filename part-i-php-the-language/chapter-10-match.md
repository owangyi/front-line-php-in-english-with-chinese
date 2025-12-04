# CHAPTER 10

## MATCH PHP 8 introduced the new match  expression - a powerful feature that will often be the better choice compared to using switch . I say "often" because both match  and switch also have specific use cases that aren't covered by the other. So what exactly are the differences? Let's start by comparing the two. Here's a classic switch  example:

```php
switch ($statusCode) {

    case 200:

    case 300:
$message = null;

        break;

    case 400:
$message = 'not found';

        break;

    case 500:
$message = 'server error';

        break;

```

    default:

```php
$message = 'unknown status code';

        break;

```

}And here is its match  equivalent:

```php
$message = match ($statusCode) {

```

    200, 300 => null,

    400 => 'not found',

    500 => 'server error',

```php
    default => 'unknown status code',

};

```

First of all, the match expression is significantly shorter:

```php
• it doesn't require a break  statement;

```

• it can combine different arms into one using a comma; and

• it returns a value, so you only have to assign the result once.

So from a syntactical point of view, match  is always easier to write. There are more dif -

ferences, though.

Expression or Statement?

I've called match  an expression, while switch  is a statement. There's indeed a difference between the two. An expression combines values and function calls, 

and is interpreted to a new value. In other words: it returns a result. This is why we can store the result of match  into a variable, while that isn't possible with switch .

No Type Coercion match  will do strict type checks instead of loose ones. It's like using === instead of ==. 

However, there might be cases where you want PHP to automatically juggle a variable's type, which explains why you can't replace all switches with matches.

```php
$statusCode = '200';
$message = match ($statusCode) {

```

    200 => null default => 'Unknown status code',

```php
};

```

// $message = 'Unknown status code'

Unknown values cause an error When there's no default  arm and when a value comes in that doesn't match any given option, PHP will throw an UnhandledMatchError  at runtime. Again more strictness, but it will prevent subtle bugs from going unnoticed.

```php
$statusCode = 400;
$message = match ($statusCode) {

```

    200 => 'perfect',

```php
};

```

// UnhandledMatchErrorOnl y Single-Line Expressions, For Now Just like short closures, you can only write one expression. Expression blocks will probably get added at one point, but it's still not clear when exactly.

Combining Conditions I already mentioned the lack of break ; this also means that match  doesn't allow for fallthrough conditions, like the two combined case  lines in the first switch  example. 

On the other hand though, you can combine conditions on the same line, separated by commas:

```php
$message = match ($statusCode) {

```

    200, 300, 301, 302 => 'combined expressions',

```php
};

```

Complex Conditions and Performance When the match  RFC was being discussed, some people suggested it wasn't necessary to add it, since the same was already possible without additional keywords but instead relying on array keys. Take this example where we want to match a value based on a more complex regex search. In here we're using the array notation some people mentioned as an alternative to match :

```php
$message = [
$this=>matchesRegex($line) => 'match A',
$this=>matchesOtherRegex($line) => 'match B',

][$search] =? 'no match';

```

But there's one big caveat: this technique will execute all regex functions first to build the array. match , on the other hand, will evaluate arm by arm, which is the more optimal approach.

Throwing Exceptions Finally, because of throw expressions in PHP 8, it's also possible to directly throw from an arm, if you'd like to.

```php
$message = match ($statusCode) {

```

    200 => null,

    500 => throw new ServerError(),

```php
    default => 'unknown status code',

```

};Pattern Matching There's one important feature still missing: proper pattern matching. It's a technique used in other programming languages to allow for intricate matching rules rather than simple comparisons. Think of it as regex, but for variables instead of text.

Pattern matching isn't supported right now because it's quite a complex feature. It has been mentioned as a future improvement for match  though. I'm already looking forward to it!

So, Switch or Match?

If I'd need to summarise the match  expression in one sentence, I'd say it's the stricter and more modern version of it's little switch  brother.

There are some cases — see what I did there? — where switch  will offer more flexibility, especially with multiline code blocks and its type juggling. On the other hand, I find the strictness of match  appealing, and the perspective of pattern matching would be a game-changer for PHP.

I admit I never wrote a switch  statement in the past because of its many quirks; quirks that match  actually solves. So while it's not perfect yet, there are use cases where match  would be a good… match.
