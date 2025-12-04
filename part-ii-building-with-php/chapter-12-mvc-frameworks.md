# CHAPTER 12

## MVC FRAMEWORKS The most popular way by far to build web applications in PHP is by using the Model View Controller (MVC) pattern. Most modern PHP frameworks build upon the same idea. At first, a request comes in and is mapped via its URL to a controller. This controller takes input from the request and passes it to the model. The model encapsu -

lates all business logic and rules of an application. The result returned from the model can be passed by the controller to the view, which is the end result returned to the user.

The benefit of the MVC pattern is its loosely coupled parts: model code can be written without having to worry about how it will be presented in the UI, and view code can be written without worrying about how exactly its data is retrieved.

Comparisons?

No framework — Symfony, Laravel, and there are lots more — is the perfect one. 

There will always be things you like more about one than another. Those prefer -

ences often originate from your past experiences, your education, the languages you've used before, other frameworks, the kinds of projects you've done, as well as your character. There's no right or wrong choice, but there is one metric I'd take into account when choosing a framework for your next project: find one that is actively maintained and has a large ecosystem surrounding it. Both Symfony and Laravel fall within this category, so really, the choice is up to you.The reason I'm only mentioning those two frameworks by the way is twofold: they are very popular within the PHP world, and I have worked personally with both of them, 

which I think is an essential requirement for me to write about them.

If you'd ask the community, they would probably say that Symfony is heavily inspired by the Java world, known for its robustness and durability. Laravel is inspired by Ruby on Rails and known for its ease-of-use and rapid application development mindset. 

This means very little, though: you can get a Symfony application up and running as fast as Laravel; the same way you can write large-scale applications with Laravel as well.

There are noticeable differences between the two. For one, the recommended code style: Laravel promotes code that's as easy as possible to read, while Symfony wants code to be written clearly and correct, even when it's more verbose. My advice to any developer regarding picking a framework is: don't lose yourself in debates over what's better or not. Both are great tools, and you can achieve the same great results with them. Also, don't try to fight the framework too much: everything is so much easier if you follow the way the framework intends you to.

Here's an example: Laravel has a powerful ORM implementation called "Eloquent".

ORMs An ORM – Object Relational Mapper — is a system that exposes the data in, for example, a database as objects in your code. It's a powerful tool that abstracts away the implementation details of database queries and allows you to think with objects instead of arrays of raw data.

Eloquent has been a highly debated topic: it uses the active record pattern which is considered to be an anti-pattern by many software developers. It's still a highly popular pattern, also in other languages, so it's definitely legit. The active record pattern breaks all the rules I've described in the previous chapter: it relies entirely on inheritance, which comes with the setbacks we already discovered. There are some other issues with it still, and here's a critique on the pattern by Robert "Uncle Bob" 

Martin:

The problem I have with Active Record is that it creates confusion about these two very different styles of programming. A database table is a data structure. 

It has exposed data and no behavior. But an Active Record appears to be an object. It has “hidden” data, and exposed behavior. I put the word “hidden” in quotes because the data is, in fact, not hidden. Almost all Active Record derivatives export the database columns through accessors and mutators.

Active record is not "correct" as defined by the rules. But Laravel has built an ex -

tremely rich API on top of it. It's by far one of the easiest ORM implementations to use. 

That is easiest for many cases, not all.

Like I said: don't fight the framework. You pick one for all the great things it provides, 

so you'll also have to deal with its little quirks and downsides. If I would write a frame -

work from scratch, I probably wouldn't use the active record pattern to build my ORM layer upon. But is it so bad that I should spend hours and days trying to change it in Laravel? No. When I use Laravel, I'm fine with using Eloquent as-is. It offers so much value in other places that it simply isn't worth fighting it.

I once worked at a company which had written their own custom framework because all popular alternatives had little quirks. This had been a company decision five years before I joined, and they made somewhere between 100 and 200 websites with it. Most were smaller company websites, but some were complex systems. As the company grew, they took on more ambitious projects and refused to work with other frameworks.More than a few of those ambitious projects failed or only partially worked because of this mentality. It also turned out their framework also had its limitations, and there was no community to fall back on. There were a few angry clients, which resulted in significant financial loss. Several colleagues — including myself — left the company because there was no room to grow in areas we believed were essential in the web development world. We were locked-in and decided to jump ship before it was too late. Finally, the company saw its mistakes and managed to switch to communi -

ty-backed frameworks, but only after they had thousands, if not millions of lines of code, all tied to their own framework — legacy that they'll have to support for years to come.

Dare to make compromises. During the first year I used Laravel, I clashed with it on many different fronts. I was used to Symfony at that point and appreciated its strict -

ness. I had a hard time adapting to Laravel, and it took me a whole year to realise I just had to stop fighting it. In the end, I embraced the framework and built on top of it, instead of trying to tear it down first partly. I learned that whatever framework or programming language you use isn't a religion; they are merely tools to help you get a job done.

Let's go back to MVC frameworks. I won't give you a step-by-step guide on setting up a Symfony or Laravel application; both communities already have excellent guidelines that cover all the topics you'll need to get started and I couldn't possibly match their quality in one chapter. Instead, I want to give you some general pointers. There's an important skill to learn when it comes to frameworks: independently finding your way around code.

Frameworks such as Laravel and Symfony have huge codebases. If you treat them like a black box, you'll never be able to use them to their full potential. It's essential to dive into source code, whether it's a framework or any other kind of codebase. It's a great skill to read code that's strange to you and follow its line of thinking. Even when you don't have any experience with a framework like Laravel or Symfony, if you're able to dive into the code to understand what's going on, you're miles ahead of many other programmers.

So let's do some code diving! I've mostly used Laravel the past three years, so I'm going to use that one as an example. Whether you have experience with it or not is irrelevant; we're interested in understanding what otherwise would be a black box. 

Because we're talking about MVC, let's look into how the request/response cycle is handled: the system that makes the MVC pattern work.

Imagine that we know absolutely nothing of this system. Where to start? Well index.php  is usually a good place:

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

As you can see, Laravel is nice enough to provide us some comments out of the box, 

explaining exactly what's going on! Personally, I find those comments a little… poetic, 

adding unnecessary noise, but we'll deal with it.This is an interesting part:

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

Some important things are happening in bootstrap/app.php , let's take a look:

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

/* … */

```php
return $app;

```

Again some comments — which I left out — and indeed, the setup of an $app  variable. 

You may or may not know what those singleton  calls are about; and that's OK for now. Based on the name of $app , we can guess that it is probably a central part of the framework, which is even made clearer given its own dedicated bootstrap file. Let's go back to index.php  first, to see how $app  is used:

```php
$kernel = $app=>make(Illuminate\Contracts\Http\Kernel=:class);
$response = $kernel=>handle(
$request = Illuminate\Http\Request=:capture()

);
$response=>send();
$kernel=>terminate($request, $response);Remember the three steps I discussed at the start of this chapter? Request to controller, controller to model and view, and that result returned as the response. All of that is happening in these lines of code:
$response = $kernel=>handle(
$request = Illuminate\Http\Request=:capture()

);
$response=>send();

```

The first step is a little hidden since it's done inline: the request is captured — it's constructed based on the $_SERVER , $_COOKIE , $_POST , and $_GET  global variables. 

Next, the captured request is passed to a kernel that handles it, which finally results in a response sent to the user.

For this example, we want to know how the controller is reached, so let's ignore the request capturing and response sending, and instead focus on the 

```php
$kernel=>handle() . There's the first real roadblock: what exactly is $kernel ? We need to know where handle  is implemented so that we can look at it.
$kernel  isn't normally instantiated, instead it's created with $app=>make()  which is given an interface Illuminate\Contracts\Http\Kernel  instead of a concrete class. 

```

There's actually two ways to solve our problem. First there's the implementation of 

```php
$app=>make() , we know that $app  is Illuminate\Foundation\Application , because it was manually constructed in the bootstrap file, so let's look over there:

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

In this case, the implementation isn't even important because the doc comment already explains what's going on: "Resolve the given type from the container". If you're unfamiliar with the dependency injection and dependency container pat -

terns, you might still need to dive deeper. Based on this comment, however, most of you probably know what's going on: we're asking $app  to make an instance of Illuminate\Contracts\Http\Kernel , which is seemingly registered in the container.That's right, we've already seen this happening in bootstrap.php :

```php
$app=>singleton(

```

    Illuminate\Contracts\Http\Kernel=:class,

    App\Http\Kernel=:class

```php
);

This definition says that when we're making Illuminate\Contracts\Http\Kernel , a concrete instance of App\Http\Kernel  should be returned! Another way to find this out would be to look at which classes implement Illuminate\Contracts\Http\Kernel ; 

```

or you can simply run the code, and inspect what object is represented in $kernel  by dumping or debugging it.

Whatever solution works best, now we know that App\Http\Kernel  is the place to look for the handle  method. And indeed, this is the right place to be.

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

This might seem like another rabbit hole at first, but we can apply the same techniques just like before. It's also good to focus on the happy path first: we can assume that's the correct way to dive. So ignore that catch  block, as well as whatever ishappening with dispatching RequestHandled  to $this=>app['events'] . Based on their names, it will dispatch an event after the request is handled.

That leaves us with only two lines of code:

```php
$request=>enableHttpMethodParameterOverride();
$response = $this=>sendRequestThroughRouter($request);

```

And reading those lines, it's clear that $this=>sendRequestThroughRouter($request)  

is where we need to go next.

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

Next we see our request sent via a pipeline through middleware, to finally be dispatched to the router. If you're familiar with MVC frameworks, route middleware prob -

ably already rings a bell. Even if you don't know about middleware we're not blocked: 

```php
$this=>dispatchToRouter()  is probably where we need to go./**

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

You can see the same pattern emerging throughout our dive. We read the code, de -

termine what's relevant and what's not, and move into the next layer. You've also seen that theoretical knowledge can help: dependency injection and middleware are two popular techniques in many MVC frameworks.

For the sake of keeping this example somewhat readable, I'm going to skip through several layers where we move from one method to another. So after going even deeper, we've arrived at Route=:run :

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

Here we see the first mention of a controller:

```php
if ($this=>isControllerAction()) {

    return $this=>runController();

```

}So now it's a matter of going one step deeper still:

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

That controller dispatcher opens a new rabbit hole! We're going to stop our dive, but you can go deeper yourself if you want to. You can apply the same techniques, and you'll very soon arrive at the actual controller code!

We did this exercise to show you that code diving shouldn't be all that difficult and is a great skill to have in your toolset. It makes you more flexible and independent as a developer and allows you to better understand and solve problems.

You can apply these code-diving techniques to every codebase, by the way, not just frameworks. I must admit that frameworks like Laravel and Symfony are generally more and better documented. We dove in rather clear waters today, but what if you need to work on a 10-year old legacy project? Well, the same techniques work just as well, but your dive will probably be much slower. Be patient, and take a break now and then.
