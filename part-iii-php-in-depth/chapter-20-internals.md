# Chapter 20: Internals

In this book, we've focussed a lot on several syntax-related and core features. Where

在这本书中，我们专注于许多与语法相关的和核心功能。这些功能来自哪里？谁决定什么被添加到语言中，什么不被添加？我之前提到过一两次"internals"（内部）组——他们是否在决定一切？

do these features come from? Who decides what gets added to the language or

确实有一群核心开发者编写和维护所有使 PHP 运行的代码。此外，还有扩展开发者、文档维护者、发布经理和其他 PHP 项目角色。所有这些人一起组成了决定什么被添加到 PHP 中，什么不被添加的组。他们是拥有投票权的人。

not? I've mentioned the "internals" group once or twice before — are they calling the

这些投票权在每个 RFC 结束时使用——"request for comments"（请求评论）。RFC 是一个描述新功能或语言更改的文档；它被讨论一段时间（最少两周），最后进行投票。如果 RFC 有 2/3 的多数票支持，它被认为被接受，功能被添加到语言中。

shots?

作为一个例子，这是 attributes RFC 的（缩短版本）。你会注意到在这个 RFC 中使用的旧属性语法，它后来才被更改。

There's indeed a group of core developers who write and maintain all code that makes

**版本：** 0.5  
**日期：** 2020-03-09  
**作者：** Benjamin Eberlei (beberlei@php.net), Martin Schröder  
**状态：** 已实现  
**目标：** 8.0  
**首次发布：** http://wiki.php.net/rfc/attributes_v2  
**实现：** https://github.com/php/php-src/pull/5394

PHP run. Additionally, there are also extension developers, documentation maintain-

这个 RFC 的很大功劳归功于 Dmitry Stogov，他之前关于 attributes 的工作是这个 RFC 和补丁的基础。

ers, release managers and other PHP project roles. All those people together form the

**介绍**

group that decides what gets added to PHP and what doesn't. They are the ones who

这个 RFC 提议将 Attributes 作为类、属性、函数、方法、参数和常量的结构化、语法元数据形式。Attributes 允许直接嵌入代码声明的配置指令。

have voting rights.

类似的概念存在于其他语言中，在 Java 中称为 Annotations，在 C#、C++、Rust、Hack 中称为 Attributes，在 Python、Javascript 中称为 Decorators。

Those voting rights are used at the end of every RFC — a "request for comments".

到目前为止，PHP 只提供这种元数据的非结构化形式：doc-comments。但 doc-comments 只是字符串，为了保持一些结构化信息，各种 PHP 子社区在它们内部发明了基于 @ 的伪语言。

An RFC is a document that describes a new feature or change to the language; it's

除了用户层面的用例之外，引擎和扩展中还有许多 attributes 的用例，这些用例可能影响编译、诊断、代码生成、运行时行为等。下面给出了示例。

discussed for a period (two weeks being the minimum), and is voted on in the end. If

用户层面 doc-comment 解析的广泛使用表明这是社区高度需求的功能。

an RFC has a 2/3 majority of votes in favour, it's considered accepted, and the feature

**提议**

is added to the language.

**属性语法**

PHP RFC: Attributes v2

Attributes 是使用现有令牌 T_SL 和 T_SR 用 "<<" 和 ">>" 包围的特殊格式文本。

As an example, here's a (shortened version) of the attributes RFC. You'll notice

attributes 可以应用于语言中的许多东西：

the old attribute syntax used in this RFC, it was changed only later.

- 函数（包括闭包和短闭包）
- 类（包括匿名类）、接口、trait
- 类常量
- 类属性
- 类方法
- 函数/方法参数

220

示例：

Version: 0.5

理论上，每个人都允许制作 RFC。你不需要有投票权。每个用户层面开发者——你和我——都可以提交一个想法供讨论。但有一个重要的注意事项：如果你设法让 RFC 被接受，它仍然需要实现。事实上，在 RFC 投票之前有一个可工作的实现通常是一个优势。所以虽然你技术上可以在 RFC 被接受后要求某人实现你的功能，但能够自己编写代码或与能够事先实现更改的人密切合作是一种资产。

Date: 2020-03-09

用几段描述了 RFC 过程后，它可能看起来相当简单和直接。当然，大多数时候，合理的 RFC 会被批准。但也有例外，RFC 可能变得非常有争议，导致冗长的讨论。最近的一个例子是 attributes RFC，我之前展示的摘录。最初被接受的 RFC 已经是添加类似注释行为的第七次尝试。那些先前的尝试发生在几年间，最早的可以追溯到 2010 年 8 月！

Author: Benjamin Eberlei (beberlei@php.net), Martin Schröder

有几个原因导致 attributes 花了十年时间才被添加。首先，有关于 attributes 应该和不应该做什么的讨论：它们支持的功能越多，实现就越复杂。有关于 attributes 应该看起来像什么，应该使用什么语法的讨论。这类问题延长了讨论期，并在此过程中导致一些失败的 RFC。不过，多年来，这个想法可以进一步改进，可能必须做出一些妥协。

Status: Implemented

这样一个妥协是 attribute 的语法，在 attributes 被接受后，花了两个额外的 RFC 来决定。有一些选项，如：@、@@、`<<>>`、`[]`，还有几个。最终，`[]` 被选为最佳选项，因为 @ 不可用，因为它已经是错误抑制运算符。需要数月的讨论才能最终达成一致同意的语法。许多好的论据被提出支持或反对所有选项。

Target: 8.0

所有这些讨论都是公开进行的。你可以通过加入 internals 邮件列表很好地跟进。有一个名为 externals.io 的网站，将邮件暴露在网页上，使它们更容易阅读。我认为关注这个列表是一件好事，稍微了解 PHP 是如何设计的。即使你从未打算为 PHP 的核心做出贡献，了解你正在使用的工具如何发展以及用户层面开发者如何在该过程中提供有价值的反馈仍然是好的。

First Published at: http://wiki.php.net/rfc/attributes_v2

我们也看到越来越多的核心贡献者在过去几年中倾听用户层面开发者。有些人坚持认为核心开发者不关心现实生活中的 PHP 的偏见，但这绝对不再是事实。核心开发者和用户层面开发者之间在社交媒体、GitHub 和 internals 列表上有很多互动。PHP 开发中的几个关键人物向用户层面开发者伸出援手，以更好地了解现实 PHP 项目中需要什么。

Implementation: https://github.com/php/php-src/pull/5394

还有改进的空间，但 PHP 在过去十年中已经成熟。这也体现在 internals 过程中。

Large credit for this RFC goes to Dmitry Stogov whose previous work on attri-

butes is the foundation for this RFC and patch.

Introduction

This RFC proposes Attributes as a form of structured, syntactic metadata to

declarations of classes, properties, functions, methods, parameters, and con-

stants. Attributes allow to define configuration directives directly embedded

with the declaration of that code.

Similar concepts exist in other languages named Annotations in Java, Attributes

in C#, C++, Rust, Hack, and Decorators in Python, Javascript.

So far, PHP only offers an unstructured form of such metadata: doc-comments.

But doc-comments are just strings, and to keep some structured informa-

tion, the @-based pseudo-language was invented inside them by various PHP

sub-communities.

On top of userland use-cases, there are many use-cases for attributes in the

engine and extensions that could affect compilation, diagnostics, code-genera-

tion, runtime behavior, and more. Examples are given below.

The widespread use of userland doc-comment parsing shows that this is a

highly demanded feature by the community.

Chapter 20 - Internals

Proposal

Attribute Syntax

Attributes are a specially formatted text enclosed with "<<" and ">>" by reusing

the existing tokens T_SL and T_SR.

attributes may be applied to many things in the language:

functions (including closures and short closures) classes (including anonymous

classes), interfaces, traits class constants class properties class methods func-

tion/method parameters

Examples:

<<ExampleAttribute>>

class Foo

{

<<ExampleAttribute>>

public const FOO = 'foo';

<<ExampleAttribute>>

public $x;

<<ExampleAttribute>>

public function foo(<<ExampleAttribute>> $bar) { }

}

…

In theory, everyone is allowed to make an RFC. You don't need to have voting rights.

Every userland developer - you and I - can submit an idea up for discussion. There is

222

an important side note, though: if you manage to get an RFC accepted, it still needs

an implementation. In fact, a working implementation before an RFC is voted on is

usually an advantage. So while you technically could ask someone to implement your

feature after your RFC is accepted, it is an asset being able to code it yourself or work

closely with someone who can implement the changes beforehand.

Having described the RFC process in a few paragraphs, it might seem pretty simple

and straightforward. Surely, most of the time, sensible RFCs get approved. But there

are exceptions where an RFC can become very controversial, with lengthy discussions

as a result. A recent example is the attributes RFC, the one I showed an excerpt from

earlier. The originally accepted RFC was already the seventh attempt to add annota-

tion-like behaviour in PHP. Those previous attempts happened over several years, the

earliest dating back to August 2010!

There are several reasons it took ten years for attributes to be added. First, there's

the discussion of what attributes should and shouldn't do: the more functionality they

support, the more complex the implementation. There's the discussion on what attri-

butes should look like, which syntax should be used. These kinds of questions length-

en discussion periods and cause a few failed RFCs along the way. Over the years

though, the idea can be polished further, and some compromises will probably have to

be made.

One such compromise is the attribute's syntax, which took two additional RFCs after

attributes were accepted to decide upon. There were options like: @, @@, =<=>, =[],

and a few more. In the end, =[] was chosen to be the best option, given that @ wasn't

available since it's already the error silencing operator. Months of discussion were

needed to arrive at an agreed upon syntax finally. Lots of good arguments have been

made in favour of and against all options.

All of these discussions happen in the open. You can follow along just fine by joining

the internals mailing list. There's a website called externals.io which exposes the mails

on a web page, making them easier to read. I think it's a good thing to follow this

list, to know a little bit about the process of how PHP is designed. Even if you never

Chapter 20 - Internals

intend to contribute to PHP's core, it's still good to know how the tools you're using

are evolving and how userland developers can provide valuable feedback within that

process.

We've also seen more and more core contributors listening to userland developers

over the past years. Some people cling to the bias that core developers don't care

about real-life PHP, but that's definitely not true anymore. There has been lots of in-

teraction between core developers and userland developers on social media, GitHub,

and the internals list. Several key figures in PHP's development reach out to userland

developers to get a better sense of what's needed in real-life PHP projects.

There's room for improvement, but PHP has been maturing over the past decade. It

also shows in the internals process.

224

