# 第十二章

## MVC 框架

到目前为止，在 PHP 中构建 Web 应用程序最流行的方法是使用模型视图控制器（MVC）模式。大多数现代 PHP 框架都基于相同的想法构建。首先，请求进入并通过其 URL 映射到控制器。该控制器从请求中获取输入并将其传递给模型。模型封装了应用程序的所有业务逻辑和规则。从模型返回的结果可以由控制器传递给视图，这是返回给用户的最终结果。

MVC 模式的好处是其松散耦合的部分：模型代码可以在不必担心它如何在 UI 中呈现的情况下编写，视图代码可以在不必担心其数据如何精确检索的情况下编写。

## 比较？

没有框架——Symfony、Laravel，还有很多——是完美的。

总会有你更喜欢一个而不是另一个的东西。这些偏好

通常源于你过去的经验、你的教育、你以前使用的语言、其他框架、你做的项目类型，以及你的性格。没有正确或错误的选择，但有一个指标我会在选择框架时考虑：找一个积极维护并有大型生态系统围绕它的框架。Symfony 和 Laravel 都属于这一类，所以真的，选择取决于你。顺便说一下，我只提到这两个框架的原因有两个：它们在 PHP 世界中非常流行，而且我个人与它们都合作过，

我认为这是我写关于它们的内容的基本要求。

如果你问社区，他们可能会说 Symfony 深受 Java 世界的启发，以其健壮性和耐用性而闻名。Laravel 受到 Ruby on Rails 的启发，以其易用性和快速应用程序开发思维而闻名。

不过，这意味着很少：你可以像 Laravel 一样快速启动和运行 Symfony 应用程序；同样，你也可以使用 Laravel 编写大规模应用程序。

两者之间有明显的差异。首先，推荐的代码风格：Laravel 提倡尽可能易于阅读的代码，而 Symfony 希望代码写得清晰正确，即使它更冗长。我对任何开发人员关于选择框架的建议是：不要迷失在关于什么更好或不好的辩论中。两者都是很好的工具，你可以用它们取得同样好的结果。另外，不要试图与框架作对太多：如果你遵循框架希望你遵循的方式，一切都会容易得多。

这里有一个例子：Laravel 有一个强大的 ORM 实现，称为"Eloquent"。

## ORM

ORM——对象关系映射器——是一个系统，它将数据（例如，数据库中的数据）作为代码中的对象公开。它是一个强大的工具，抽象了数据库查询的实现细节，允许你使用对象而不是原始数据数组来思考。

Eloquent 一直是一个备受争议的话题：它使用活动记录模式，这被许多软件开发人员认为是反模式。它仍然是一个非常流行的模式，在其他语言中也是如此，所以它绝对是合法的。活动记录模式打破了我在前一章中描述的所有规则：它完全依赖继承，这带来了我们已经发现的挫折。它仍然存在一些其他问题，这里是 Robert "Uncle Bob"

Martin 对该模式的批评：

我对活动记录的问题是，它在这两种非常不同的编程风格之间造成了混淆。数据库表是一种数据结构。

它有公开的数据，没有行为。但活动记录看起来像一个对象。它有"隐藏"的数据和公开的行为。我把"隐藏"这个词放在引号中，因为数据实际上并没有隐藏。几乎所有活动记录的衍生品都通过访问器和修改器导出数据库列。

活动记录按照规则定义不是"正确的"。但 Laravel 在其基础上构建了一个极其丰富的 API。它是迄今为止最容易使用的 ORM 实现之一。

这对许多情况来说是最容易的，但不是全部。

就像我说的：不要与框架作对。你选择一个框架是因为它提供的所有好东西，

所以你也必须处理它的小怪癖和缺点。如果我从头开始编写框架，我可能不会使用活动记录模式来构建我的 ORM 层。但它是否如此糟糕，以至于我应该花费数小时和数天试图在 Laravel 中改变它？不。当我使用 Laravel 时，我很乐意按原样使用 Eloquent。它在其他地方提供了如此多的价值，以至于根本不值得与它作对。

我曾经在一家公司工作，该公司编写了自己的自定义框架，因为所有流行的替代方案都有小怪癖。这是在我加入之前五年的公司决定，他们用它制作了大约 100 到 200 个网站。大多数是较小的公司网站，但有些是复杂的系统。随着公司的发展，他们承担了更雄心勃勃的项目，并拒绝与其他框架合作。由于这种心态，这些雄心勃勃的项目中有不少失败了或只部分工作。结果证明他们的框架也有其局限性，没有社区可以依靠。有一些愤怒的客户，这导致了重大的财务损失。包括我在内的几位同事离开了公司，因为在我们认为对 Web 开发世界至关重要的领域没有成长空间。我们被锁定了，并决定在为时已晚之前跳槽。最后，公司看到了它的错误，并设法切换到社区支持的框架，但只有在他们有数千甚至数百万行代码之后，所有这些都绑定到他们自己的框架——他们将在未来几年必须支持的遗留代码。

敢于做出妥协。在我使用 Laravel 的第一年，我在许多不同的方面与它发生了冲突。那时我已经习惯了 Symfony 并欣赏它的严格性。

我很难适应 Laravel，我花了整整一年才意识到我只需要停止与它作对。最后，我接受了框架并在其上构建，而不是试图先部分拆除它。我了解到，无论你使用什么框架或编程语言都不是宗教；它们只是帮助你完成工作的工具。

让我们回到 MVC 框架。我不会给你一个关于设置 Symfony 或 Laravel 应用程序的分步指南；两个社区都已经有优秀的指南，涵盖了所有你需要开始的主题，我不可能在某一章中匹配它们的质量。相反，我想给你一些一般性的建议。在框架方面，有一个重要的技能需要学习：独立地在代码中找到你的方式。

像 Laravel 和 Symfony 这样的框架有巨大的代码库。如果你将它们视为黑盒，你将永远无法充分利用它们。深入研究源代码是必不可少的，无论是框架还是任何其他类型的代码库。阅读对你来说陌生的代码并遵循其思路是一项很好的技能。即使你对像 Laravel 或 Symfony 这样的框架没有任何经验，如果你能够深入研究代码以了解发生了什么，你就领先于许多其他程序员。

所以让我们做一些代码探索！我过去三年主要使用 Laravel，所以我将用它作为例子。无论你是否有经验都无关紧要；我们感兴趣的是理解否则将是黑盒的东西。

因为我们正在讨论 MVC，让我们看看如何处理请求/响应周期：使 MVC 模式工作的系统。

想象一下，我们对这个系统一无所知。从哪里开始？嗯，index.php 通常是一个好地方：

/**

 * Laravel - A PHP Framework For Web Artisans

 *

 * @package  Laravel

 * @author   Taylor Otwell <taylor@laravel.com>

 */

define('LARAVEL_START', microtime(true));/*

|----------------------------------------------------------------------

| Register The Auto Loader

|----------------------------------------------------------------------

|

| Composer provides a convenient, automatically generated class loader for

| our application. We just need to utilize it! We'll simply require it

| into the script here so that we don't have to worry about manual

| loading any of our classes later on. It feels great to relax.

|

*/

```php
require =_DIR=_.'/=./vendor/autoload.php';

```

/*

|----------------------------------------------------------------------

| Turn On The Lights

|----------------------------------------------------------------------

|

| We need to illuminate PHP development, so let us turn on the lights.

| This bootstraps the framework and gets it ready for use, then it

| will load up this application so that we can run it and send

| the responses back to the browser and delight our users.

|

*/

```php
$app = require_once =_DIR=_.'/=./bootstrap/app.php';

```

/*

|----------------------------------------------------------------------

| Run The Application

|----------------------------------------------------------------------

|

| Once we have the application, we can handle the incoming request

| through the kernel, and send the associated response back to

| the client's browser allowing them to enjoy the creative

| and wonderful application we have prepared for them.

|

*/

```php
$kernel = $app=>make(Illuminate\Contracts\Http\Kernel=:class);
$response = $kernel=>handle(
$request = Illuminate\Http\Request=:capture()

);
$response=>send();
$kernel=>terminate($request, $response);

```

正如你所看到的，Laravel 足够好，为我们提供了一些开箱即用的注释，

准确解释了正在发生的事情！就我个人而言，我发现这些注释有点……诗意，

添加了不必要的噪音，但我们会处理它。这是一个有趣的部分：

/*

| …

|

| This bootstraps the framework and gets it ready for use, then it

| will load up this application so that we can run it and send

| the responses back to the browser and delight our users.

|

*/

```php
$app = require_once =_DIR=_.'/=./bootstrap/app.php';

```

一些重要的事情发生在 bootstrap/app.php 中，让我们看看：

/* … */

```php
$app = new Illuminate\Foundation\Application(
$_ENV['APP_BASE_PATH'] =? dirname(=_DIR=_)

);

```

/* … */

```php
$app=>singleton(

```

    Illuminate\Contracts\Http\Kernel=:class,

    App\Http\Kernel=:class

```php
);
$app=>singleton(

```

    Illuminate\Contracts\Console\Kernel=:class,

    App\Console\Kernel=:class

```php
);
$app=>singleton(

```

    Illuminate\Contracts\Debug\ExceptionHandler=:class,

    App\Exceptions\Handler=:class

```php
);

```

再次一些注释——我遗漏了——确实，$app 变量的设置。

你可能知道也可能不知道那些 singleton 调用是关于什么的；现在这没关系。基于 $app 的名称，我们可以猜测它可能是框架的核心部分，考虑到它自己的专用引导文件，这一点更加清楚。让我们先回到 index.php，看看 $app 是如何使用的：

```php
$kernel = $app=>make(Illuminate\Contracts\Http\Kernel=:class);
$response = $kernel=>handle(
$request = Illuminate\Http\Request=:capture()

);
$response=>send();
$kernel=>terminate($request, $response);记住我在本章开头讨论的三个步骤吗？请求到控制器，控制器到模型和视图，以及该结果作为响应返回。所有这些都发生在这几行代码中：

$response = $kernel=>handle(
$request = Illuminate\Http\Request=:capture()

);
$response=>send();

```

第一步有点隐藏，因为它是内联完成的：请求被捕获——它是基于 $_SERVER、$_COOKIE、$_POST 和 $_GET 全局变量构造的。

接下来，捕获的请求被传递给处理它的内核，最终结果是发送给用户的响应。

对于这个例子，我们想知道如何到达控制器，所以让我们忽略请求捕获和响应发送，而是专注于

```php
$kernel=>handle()。这是第一个真正的障碍：$kernel 到底是什么？我们需要知道 handle 在哪里实现，这样我们就可以查看它。

$kernel 通常不会实例化，而是使用 $app=>make() 创建的，它被赋予一个接口 Illuminate\Contracts\Http\Kernel 而不是具体类。

```

实际上有两种方法可以解决我们的问题。首先是

```php
$app=>make() 的实现，我们知道 $app 是 Illuminate\Foundation\Application，因为它在引导文件中手动构造，所以让我们看看那里：

```

/**

 * Resolve the given type from the container.

 *

 * @param  string  $abstract

 * @param  array  $parameters

 * @return mixed

 */

```php
public function make($abstract, array $parameters = [])

{
$this=>loadDeferredProviderIfNeeded(
$abstract = $this=>getAlias($abstract)

    );

    return parent=:make($abstract, $parameters);

}

```

在这种情况下，实现甚至不重要，因为文档注释已经解释了正在发生的事情："从容器中解析给定类型"。如果你不熟悉依赖注入和依赖容器模式，你可能仍然需要深入研究。然而，基于这个注释，你们大多数人可能知道发生了什么：我们要求 $app 创建 Illuminate\Contracts\Http\Kernel 的实例，它似乎注册在容器中。没错，我们已经看到这发生在 bootstrap.php 中：

```php
$app=>singleton(

```

    Illuminate\Contracts\Http\Kernel=:class,

    App\Http\Kernel=:class

```php
);

```

这个定义说当我们创建 Illuminate\Contracts\Http\Kernel 时，应该返回 App\Http\Kernel 的具体实例！找出这一点的另一种方法是查看哪些类实现了 Illuminate\Contracts\Http\Kernel；

```php
或者你可以简单地运行代码，并通过转储或调试它来检查 $kernel 中表示的对象。

```

无论什么解决方案最有效，现在我们知道 App\Http\Kernel 是查找 handle 方法的地方。确实，这是正确的地方。

/**

 * Handle an incoming HTTP request.

 *

 * @param  \Illuminate\Http\Request  $request

 * @return \Illuminate\Http\Response

 */

```php
public function handle($request)

{

    try {
$request=>enableHttpMethodParameterOverride();
$response = $this=>sendRequestThroughRouter($request);

    } catch (Throwable $e) {
$this=>reportException($e);
$response = $this=>renderException($request, $e);

    }
$this=>app['events']=>dispatch(

        new RequestHandled($request, $response)

    );

    return $response;

}

```

这乍一看可能像是另一个兔子洞，但我们可以像以前一样应用相同的技术。首先专注于快乐路径也是好的：我们可以假设这是正确的探索方式。所以忽略那个 catch 块，以及将 RequestHandled 分派到 $this=>app['events'] 时发生的任何事情。基于它们的名称，它将在请求处理后分派一个事件。

这给我们留下了只有两行代码：

```php
$request=>enableHttpMethodParameterOverride();
$response = $this=>sendRequestThroughRouter($request);

```

阅读这些行，很明显 $this=>sendRequestThroughRouter($request)

是我们下一步需要去的地方。

/**

 * Send the given request through the middleware / router.

 *

 * @param  \Illuminate\Http\Request  $request

 * @return \Illuminate\Http\Response

 */

```php
protected function sendRequestThroughRouter($request)

{
$this=>app=>instance('request', $request);

    Facade=:clearResolvedInstance('request');
$this=>bootstrap();

    return (new Pipeline($this=>app))

```

                =>send($request)

                =>through(

```php
$this=>app=>shouldSkipMiddleware() 

```

                        ? [] 

                        : $this=>middleware

                )

```php
                =>then($this=>dispatchToRouter());

}

```

接下来我们看到我们的请求通过管道通过中间件发送，最终被分派到路由器。如果你熟悉 MVC 框架，路由中间件可能已经让你想起了什么。即使你不知道中间件，我们也不会被阻止：

```php
$this=>dispatchToRouter() 可能是我们需要去的地方。

/**

```

 * Get the route dispatcher callback.

 *

 * @return \Closure

 */

```php
protected function dispatchToRouter()

{

    return function ($request) {
$this=>app=>instance('request', $request);

        return $this=>router=>dispatch($request);

    };

}

```

你可以看到相同的模式在我们的探索中不断出现。我们阅读代码，确定什么是相关的，什么不是，然后进入下一层。你也看到理论知识可以帮助：依赖注入和中间件是许多 MVC 框架中的两种流行技术。

为了保持这个例子的可读性，我将跳过几层，从一种方法移动到另一种方法。所以在更深入之后，我们到达了 Route=:run：

/**

 * Run the route action and return the response.

 *

 * @return mixed

 */

```php
public function run()

{
$this=>container = $this=>container =: new Container;

    try {

        if ($this=>isControllerAction()) {

            return $this=>runController();

        }

        return $this=>runCallable();

    } catch (HttpResponseException $e) {

        return $e=>getResponse();

    }

}

```

这里我们第一次提到控制器：

```php
if ($this=>isControllerAction()) {

    return $this=>runController();

```

}所以现在仍然需要再深入一步：

/**

 * Run the route action and return the response.

 *

 * @return mixed

 *

 * @throws \Symfony\Component\HttpKernel\Exception\NotFoundHttpException

 */

```php
protected function runController()

{

    return $this=>controllerDispatcher()=>dispatch(
$this, $this=>getController(), $this=>getControllerMethod()

    );

}

```

那个控制器分派器打开了一个新的兔子洞！我们将停止我们的探索，但如果你想的话，你可以自己更深入。你可以应用相同的技术，很快你就会到达实际的控制器代码！

我们做这个练习是为了向你展示代码探索不应该那么困难，并且是你在工具集中拥有的很好的技能。它使你作为开发人员更加灵活和独立，并允许你更好地理解和解决问题。

顺便说一下，你可以将这些代码探索技术应用到每个代码库，不仅仅是框架。我必须承认，像 Laravel 和 Symfony 这样的框架通常有更多更好的文档。我们今天在相当清晰的水域中探索，但如果你需要在一个有 10 年历史的遗留项目上工作呢？嗯，相同的技术同样有效，但你的探索可能会慢得多。要有耐心，时不时休息一下。

