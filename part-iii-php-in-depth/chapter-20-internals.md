# CHAPTER 20

## INTERNALS In this book, we've focussed a lot on several syntax-related and core features. Where do these features come from? Who decides what gets added to the language or not? I've mentioned the "internals" group once or twice before — are they calling the shots?

There's indeed a group of core developers who write and maintain all code that makes PHP run. Additionally, there are also extension developers, documentation maintain -

ers, release managers and other PHP project roles. All those people together form the group that decides what gets added to PHP and what doesn't. They are the ones who have voting rights.

Those voting rights are used at the end of every RFC — a "request for comments". 

An RFC is a document that describes a new feature or change to the language; it's discussed for a period (two weeks being the minimum), and is voted on in the end. If an RFC has a 2/3 majority of votes in favour, it's considered accepted, and the feature is added to the language.

PHP RFC: Attributes v2 As an example, here's a (shortened version) of the attributes RFC. You'll notice the old attribute syntax used in this RFC, it was changed only later.Version: 0.5 Date: 2020-03-09 Author: Benjamin Eberlei ( beberlei@php.net ), Martin Schröder Status: Implemented Target: 8.0 First Published at: http://wiki.php.net/rfc/attributes_v2 Implementation: https://github.com/php/php-src/pull/5394 Large credit for this RFC goes to Dmitry Stogov whose previous work on attributes is the foundation for this RFC and patch.

Introduction This RFC proposes Attributes as a form of structured, syntactic metadata to declarations of classes, properties, functions, methods, parameters, and constants. Attributes allow to define configuration directives directly embedded with the declaration of that code.

Similar concepts exist in other languages named Annotations in Java, Attributes in C#, C++, Rust, Hack, and Decorators in Python, Javascript.

So far, PHP only offers an unstructured form of such metadata: doc-comments. 

But doc-comments are just strings, and to keep some structured information, the @-based pseudo-language was invented inside them by various PHP sub-communities.

On top of userland use-cases, there are many use-cases for attributes in the engine and extensions that could affect compilation, diagnostics, code-genera -

tion, runtime behavior, and more. Examples are given below.

The widespread use of userland doc-comment parsing shows that this is a highly demanded feature by the community.

Proposal Attribute Syntax Attributes are a specially formatted text enclosed with "<<" and ">>" by reusing the existing tokens T_SL and T_SR.

attributes may be applied to many things in the language:

functions (including closures and short closures) classes (including anonymous classes), interfaces, traits class constants class properties class methods func -

tion/method parameters Examples:

<<ExampleAttribute>>

```php
class Foo

{

```

    <<ExampleAttribute>>

```php
    public const FOO = 'foo';

 

```

    <<ExampleAttribute>>

```php
    public $x;

 

```

    <<ExampleAttribute>>

```php
    public function foo(<<ExampleAttribute>> $bar) { }

}

```

…

In theory, everyone is allowed to make an RFC. You don't need to have voting rights. 

Every userland developer - you and I - can submit an idea up for discussion. There isan important side note, though: if you manage to get an RFC accepted, it still needs an implementation. In fact, a working implementation before an RFC is voted on is usually an advantage. So while you technically could ask someone to implement your feature after your RFC is accepted, it is an asset being able to code it yourself or work closely with someone who can implement the changes beforehand.

Having described the RFC process in a few paragraphs, it might seem pretty simple and straightforward. Surely, most of the time, sensible RFCs get approved. But there are exceptions where an RFC can become very controversial, with lengthy discussions as a result. A recent example is the attributes RFC, the one I showed an excerpt from earlier. The originally accepted RFC was already the seventh attempt to add annota -

tion-like behaviour in PHP. Those previous attempts happened over several years, the earliest dating back to August 2010!

There are several reasons it took ten years for attributes to be added. First, there's the discussion of what attributes should and shouldn't do: the more functionality they support, the more complex the implementation. There's the discussion on what attri -

butes should look like, which syntax should be used. These kinds of questions lengthen discussion periods and cause a few failed RFCs along the way. Over the years though, the idea can be polished further, and some compromises will probably have to be made.

One such compromise is the attribute's syntax, which took two additional RFCs after attributes were accepted to decide upon. There were options like: @, @@, =<=> , =[], 

and a few more. In the end, =[] was chosen to be the best option, given that @ wasn't available since it's already the error silencing operator. Months of discussion were needed to arrive at an agreed upon syntax finally. Lots of good arguments have been made in favour of and against all options.

All of these discussions happen in the open. You can follow along just fine by joining the internals mailing list. There's a website called externals.io which exposes the mails on a web page, making them easier to read. I think it's a good thing to follow this list, to know a little bit about the process of how PHP is designed. Even if you never intend to contribute to PHP's core, it's still good to know how the tools you're using are evolving and how userland developers can provide valuable feedback within that process.

We've also seen more and more core contributors listening to userland developers over the past years. Some people cling to the bias that core developers don't care about real-life PHP, but that's definitely not true anymore. There has been lots of interaction between core developers and userland developers on social media, GitHub, 

and the internals list. Several key figures in PHP's development reach out to userland developers to get a better sense of what's needed in real-life PHP projects.

There's room for improvement, but PHP has been maturing over the past decade. It also shows in the internals process.
