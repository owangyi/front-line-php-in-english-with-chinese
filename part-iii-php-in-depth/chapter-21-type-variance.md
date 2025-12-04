# CHAPTER 21

## TYPE VARIANCE Earlier in this book, we talked about type systems and their value to a programming language. We also spoke about recent changes to PHP's type system and how it's made more flexible by adding proper variance support. Type safety in programming languages is such an interesting topic that I decided to spend a dedicated chapter on it.

When we talked about static analysis, I showed the example of an RgbValue  class to represent "integer values between 0 and 255". This type ensures valid input and allows us to remove redundant input validation. It looked like this:

```php
class RgbValue extends MinMaxInt

{

    public function =_construct(int $value) 

    {

        parent=:=_construct(0, 255, $value);

    }

}

```

Using RgbValue  as a type, we're promised we'll only be passed input to our function that's within the subset it describes. Subset is the interesting word here. All types can be thought of as a filter on all available input. RgbValue  represents a subset of positive integers, which represents a subset of all integers, which in turn is a subset of all scalar values (integers, floats, strings, …), which are a subset of ev-erything. Can you see the mental image of some kind of inheritance chain forming? 

RgbValue > positive ints > all ints > scalar values > everything .

Here's another example: When we talked about PHP's type system, we had a class called UnknownDate ; it represented a missing date and allowed us to use the null object pattern. UnknownDate  is as subtype of Date , which is a subtype of object , which again is a subtype of everything.

Speaking of that example, let's revisit it. Here's the Invoice  interface:

```php
interface Invoice

{

    public function getPaymentDate(): Date;

}

```

This interface represents the Invoice  type, and it comes with a rule: it has a PaymentDate . This interface promises  that any object implementing Invoice  will return a valid Date  object when calling getPaymentDate() . So what about PendingInvoice ? 

We decided to make it return an UnknownDate . This raises the question: does the promise made by the Invoice  interface still hold?

```php
class PendingInvoice implements Invoice

{

    public function getPaymentDate(): UnknownDate 

    {

        return new UnknownDate();

    }

}

```

It sure does! Since all unknown dates are a subset  of dates, it means that whenever an UnknownDate  is returned, we're always sure it's also a Date . This is what variance describes: type definitions that change during inheritance, which still fulfill the par -

ent's original promise. In the case of return types, we're allowed to further specify them during inheritance, which is called "covariance". In the case of argument types, 

the opposite is true.

It isn't easy to come up with an example that makes sense for contravariant types — 

the opposite of covariant types. They are only rarely used in PHP: they make most sense combined with generics, which PHP doesn't support.

Still, there are a few edge cases where contravariance might be useful. Let's consider an example:

```php
interface Repository

{

    public function retrieve(int $id): object;

    public function store(object $object): void;

}

interface WithUuid

{

    public function retrieve(string $uuid): object;

}

```

The Repository  interface describes a simplified repository: a class that can retrieve and store objects from a data store. The repository assumes all IDs will be integers.There's also a WithUuid  interface though, one that allows passing textual UUIDs instead of numbers. Next let's implement the OrderRepository :

```php
class OrderRepository implements Repository, WithUuid

{

    public function retrieve(int $id): object { /* … */ }

    public function store(object $object): void { /* … */ }

}

```

Here we see a problem: we can't use int $id  in the retrieve  method, because it violates the contract specified by WithUuid . If we'd use string $uuid , there would be the same problem but the other way around.

It's those edge cases that make contravariant types useful: PHP allows us to widen argument types, in order to fulfil both promises: one made by Repository , and one made by WithUuid . Thanks to PHP 8's union types, we can write retrieve 's imple -

mentation like so:

```php
class OrderRepository implements Repository, WithUuid

{

    public function retrieve(int|string $id): object { /* … */ }

    

```

    // …

```php
}

```

And this code works! Of course, we need to manually deal with managing both strings and integers in our retrieve method now; still, it's good to have the option available when there's no way around the problem.

So return types are covariant, argument types contravariant. What about typed properties? They are invariant, which means you're not allowed to change property types during inheritance. It is explained clearly in the typed properties RFC why that is: 

"The reason why property types are invariant is that they can be both read from and written to. The change from int to ?int  implies that reads from the property may now also return null  in addition to integers. The change from ?int  to int implies that it is no longer possible to write null  to the property. As such, neither contravariance nor covariance are applicable to property types."

Before PHP 7.4, you weren't allowed to widen or narrow types, even though it would be technically correct. And while it might seem like a minor change, it's actually one that makes PHP's type system much more flexible to use.
