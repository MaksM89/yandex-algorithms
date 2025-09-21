# https://api.contest.yandex.net/api/public/v2/contests/53029/problems
problems = {
    'problems': [
        {
            'compilers': [
                'haskell',
                'gcc_cpp20',
                'gcc_c17',
                'golang_docker',
                'nodejs_18',
                'ruby2',
                'fpc30',
                'dart_2_14',
                'jdk20',
                'pascal_abc',
                'pypy3_7_1_0',
                'kotlin_1_8_0',
                'python3_docker',
                'swift-5_1',
                'rust154',
                'scala_docker',
                'perl',
                'php8_1',
                'dotnet6_asp'
            ],
            'alias': 'E',
            'id': '30404/2018_03_13/iKfA2wqYmA',
            'name': 'Поразрядная сортировка',
            'statements': [
                {
                  'type': 'TEX',
                  'locale': 'ru',
                  'path': 'statements/.html/ru/full_page.html'
                }
            ],
            'limits': [
                {
                    'compilerName': 'Others',
                    'timeLimit': 1000,
                    'idlenessLimit': 10000,
                    'memoryLimit': 67108864,
                    'outputLimit': 67108864
                }
            ],
            'testCount': None,
            'problemType': 'PROBLEM_WITH_CHECKER'
        },
        {
            'compilers': [
                'haskell',
                'gcc_cpp20',
                'gcc_c17',
                'golang_docker',
                'nodejs_18',
                'ruby2',
                'fpc30',
                'dart_2_14',
                'jdk20',
                'pascal_abc',
                'pypy3_7_1_0',
                'kotlin_1_8_0',
                'python3_docker',
                'swift-5_1',
                'rust154',
                'scala_docker',
                'perl',
                'php8_1',
                'dotnet6_asp'
            ],
            'alias': 'D',
            'id': '4105/2015_01_14/95CAAPxq5L',
            'name': 'Сортировка слиянием',
            'statements': [
                {
                    'type': 'TEX',
                    'locale': 'ru',
                    'path': 'statements/.html/ru/full_page.html'
                }
            ],
            'limits': [
                {
                    'compilerName': 'Others',
                    'timeLimit': 15000,
                    'idlenessLimit': 15000,
                    'memoryLimit': 536870912,
                    'outputLimit': 67108864
                }
            ],
            'testCount': None,
            'problemType': 'PROBLEM_WITH_CHECKER'
        },
        {
            'compilers': [
                'haskell',
                'gcc_cpp20',
                'gcc_c17',
                'golang_docker',
                'nodejs_18',
                'ruby2',
                'fpc30',
                'dart_2_14',
                'jdk20',
                'pascal_abc',
                'pypy3_7_1_0',
                'kotlin_1_8_0',
                'python3_docker',
                'swift-5_1',
                'rust154',
                'scala_docker',
                'perl',
                'php8_1',
                'dotnet6_asp'
            ],
            'alias': 'B',
            'id': '4105/2015_01_14/9DYI7g2bpQ',
            'name': 'Быстрая сортировка',
            'statements': [
                {
                    'type': 'TEX',
                    'locale': 'ru',
                    'path': 'statements/.html/ru/full_page.html'
                }
            ],
            'limits': [
                {
                    'compilerName': 'Others',
                    'timeLimit': 10000,
                    'idlenessLimit': 15000,
                    'memoryLimit': 536870912,
                    'outputLimit': 67108864
                }
            ],
            'testCount': None,
            'problemType': 'PROBLEM_WITH_CHECKER'
        },
        {
            'compilers': [
                'haskell',
                'gcc_cpp20',
                'gcc_c17',
                'golang_docker',
                'nodejs_18',
                'ruby2',
                'fpc30',
                'dart_2_14',
                'jdk20',
                'pascal_abc',
                'pypy3_7_1_0',
                'kotlin_1_8_0',
                'python3_docker',
                'swift-5_1',
                'rust154',
                'scala_docker',
                'perl',
                'php8_1',
                'dotnet6_asp'
            ],
            'alias': 'A',
            'id': '4105/2015_01_14/BJQFReu5iY',
            'name': 'Partition',
            'statements': [
                {
                    'type': 'TEX',
                    'locale': 'ru',
                    'path': 'statements/.html/ru/full_page.html'
                }
            ],
            'limits': [
                {
                    'compilerName': 'Others',
                    'timeLimit': 2000,
                    'idlenessLimit': 10000,
                    'memoryLimit': 268435456,
                    'outputLimit': 67108864
                }
            ],
            'testCount': None,
            'problemType': 'PROBLEM_WITH_CHECKER'
        },
        {
            'compilers': [
                'haskell',
                'gcc_cpp20',
                'gcc_c17',
                'golang_docker',
                'nodejs_18',
                'ruby2',
                'fpc30',
                'dart_2_14',
                'jdk20',
                'pascal_abc',
                'pypy3_7_1_0',
                'kotlin_1_8_0',
                'python3_docker',
                'swift-5_1',
                'rust154',
                'scala_docker',
                'perl',
                'php8_1',
                'dotnet6_asp'
            ],
            'alias': 'C',
            'id': '4105/2015_01_14/BJoIIyloBm',
            'name': 'Слияние',
            'statements': [
                {
                    'type': 'TEX',
                    'locale': 'ru',
                    'path': 'statements/.html/ru/full_page.html'
                }
            ],
            'limits': [
                {
                    'compilerName': 'Others',
                    'timeLimit': 5000,
                    'idlenessLimit': 10000,
                    'memoryLimit': 536870912,
                    'outputLimit': 67108864
                }
            ],
            'testCount': None,
            'problemType': 'PROBLEM_WITH_CHECKER'
        }
    ]
}

# 'https://api.contest.yandex.net/api/public/v2/contests/53029/problems/A/statement'
file_content = r"""
<!DOCTYPE html
  SYSTEM "html">
<div class="problem-statement">
   <div class="header">
      <h1 class="title">Partition</h1>
      <table>
         <tr class="time-limit">
            <td class="property-title">Ограничение времени</td>
            <td>2&nbsp;секунды</td>
         </tr>
         <tr class="memory-limit">
            <td class="property-title">Ограничение памяти</td>
            <td>256Mb</td>
         </tr>
         <tr class="input-file">
            <td class="property-title">Ввод</td>
            <td colspan="1">стандартный ввод или input.txt</td>
         </tr>
         <tr class="output-file">
            <td class="property-title">Вывод</td>
            <td colspan="1">стандартный вывод или output.txt</td>
         </tr>
      </table>
   </div>
   <h2></h2>
   <div class="legend"><p>Базовым алгоритмом для быстрой сортировки является алгоритм partition, который разбивает набор элементов на две части относительно
      заданного предиката.<br> По сути элементы массива просто меняются местами так, что левее некоторой точки в нем после этой
      операции лежат элементы, удовлетворяющие заданному предикату, а справа — не удовлетворяющие ему.<br> Например, при сортировке
      можно использовать предикат «меньше опорного», что при оптимальном выборе опорного элемента может разбить массив на две примерно
      равные части.</p>
      <p>Напишите алгоритм partition в качестве первого шага для написания быстрой сортировки.</p>
   </div>
   <h2>Формат ввода</h2>
   <div class="input-specification"><p>В первой строке входного файла содержится число <span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mi>
      N
      </mi>
      </mrow>
      <annotation encoding="application/x-tex">
      N
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span
      class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span></span> — количество элементов массива
      (<span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mn>
      0
      </mn>
      <mo>
      ≤
      </mo>
      <mi>
      N
      </mi>
      <mo>
      ≤
      </mo>
      <mn>
      1
      </mn>
      <msup>
      <mn>
      0
      </mn>
      <mn>
      6
      </mn>
      </msup>
      </mrow>
      <annotation encoding="application/x-tex">
      0 \leq N \leq 10^6
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.7804em;vertical-align:-0.136em;"></span><span
      class="mord">0</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≤</span><span class="mspace"
      style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut" style="height:0.8193em;vertical-align:-0.136em;"></span><span
      class="mord mathnormal" style="margin-right:0.10903em;">N</span><span class="mspace" style="margin-right:0.2778em;"></span><span
      class="mrel">≤</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="strut"
      style="height:0.8141em;"></span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span class="msupsub"><span
      class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span
      class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">6</span></span></span></span></span></span></span></span></span></span></span></span>).<br>
      Во второй строке содержатся <span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mi>
      N
      </mi>
      </mrow>
      <annotation encoding="application/x-tex">
      N
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.6833em;"></span><span
      class="mord mathnormal" style="margin-right:0.10903em;">N</span></span></span></span></span> целых чисел <span class="math
      inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <msub>
      <mi>
      a
      </mi>
      <mi>
      i
      </mi>
      </msub>
      </mrow>
      <annotation encoding="application/x-tex">
      a_i
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.5806em;vertical-align:-0.15em;"></span><span
      class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span
      class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut"
      style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight">i</span></span></span></span><span
      class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span></span></span></span></span>,
      разделенных пробелами (<span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mo>
      −
      </mo>
      <mn>
      1
      </mn>
      <msup>
      <mn>
      0
      </mn>
      <mn>
      9
      </mn>
      </msup>
      <mo>
      ≤
      </mo>
      <msub>
      <mi>
      a
      </mi>
      <mi>
      i
      </mi>
      </msub>
      <mo>
      ≤
      </mo>
      <mn>
      1
      </mn>
      <msup>
      <mn>
      0
      </mn>
      <mn>
      9
      </mn>
      </msup>
      </mrow>
      <annotation encoding="application/x-tex">
      -10^9 \leq a_i \leq 10^9
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.9501em;vertical-align:-0.136em;"></span><span
      class="mord">−</span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span class="msupsub"><span
      class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span
      class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">9</span></span></span></span></span></span></span></span><span
      class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≤</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span
      class="base"><span class="strut" style="height:0.786em;vertical-align:-0.15em;"></span><span class="mord"><span class="mord
      mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3117em;"><span
      style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing
      reset-size6 size3 mtight"><span class="mord mathnormal mtight">i</span></span></span></span><span class="vlist-s">​</span></span><span
      class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span><span class="mspace"
      style="margin-right:0.2778em;"></span><span class="mrel">≤</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span
      class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span
      class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span
      class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">9</span></span></span></span></span></span></span></span></span></span></span></span>).<br>
      В третьей строке содержится опорный элемент <span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mi>
      x
      </mi>
      </mrow>
      <annotation encoding="application/x-tex">
      x
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.4306em;"></span><span
      class="mord mathnormal">x</span></span></span></span></span> (<span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mo>
      −
      </mo>
      <mn>
      1
      </mn>
      <msup>
      <mn>
      0
      </mn>
      <mn>
      9
      </mn>
      </msup>
      <mo>
      ≤
      </mo>
      <mi>
      x
      </mi>
      <mo>
      ≤
      </mo>
      <mn>
      1
      </mn>
      <msup>
      <mn>
      0
      </mn>
      <mn>
      9
      </mn>
      </msup>
      </mrow>
      <annotation encoding="application/x-tex">
      -10^9 \leq x \leq 10^9
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.9501em;vertical-align:-0.136em;"></span><span
      class="mord">−</span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span class="msupsub"><span
      class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span
      class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">9</span></span></span></span></span></span></span></span><span
      class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≤</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span
      class="base"><span class="strut" style="height:0.7719em;vertical-align:-0.136em;"></span><span class="mord mathnormal">x</span><span
      class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">≤</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span
      class="base"><span class="strut" style="height:0.8141em;"></span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span
      class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.8141em;"><span style="top:-3.063em;margin-right:0.05em;"><span
      class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">9</span></span></span></span></span></span></span></span></span></span></span></span>).<br>
      Заметьте, что <span class="math inline"><span class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <mi>
      x
      </mi>
      </mrow>
      <annotation encoding="application/x-tex">
      x
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.4306em;"></span><span
      class="mord mathnormal">x</span></span></span></span></span> не обязательно встречается среди <span class="math inline"><span
      class="katex"><span class="katex-mathml">
      <math xmlns="http://www.w3.org/1998/Math/MathML">
      <semantics>
      <mrow>
      <msub>
      <mi>
      a
      </mi>
      <mi>
      i
      </mi>
      </msub>
      </mrow>
      <annotation encoding="application/x-tex">
      a_i
      </annotation>
      </semantics>
      </math></span><span class="katex-html" aria-hidden="true"><span class="base"><span class="strut" style="height:0.5806em;vertical-align:-0.15em;"></span><span
      class="mord"><span class="mord mathnormal">a</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span
      class="vlist" style="height:0.3117em;"><span style="top:-2.55em;margin-left:0em;margin-right:0.05em;"><span class="pstrut"
      style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mathnormal mtight">i</span></span></span></span><span
      class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span></span></span></span></span></span>.</p>
   </div>
   <h2>Формат вывода</h2>
   <div class="output-specification"><p>Выведите результат работы вашего алгоритма при использовании предиката «меньше x»: в первой строке выведите число элементов
      массива, меньших x, а во второй — количество всех остальных.</p>
   </div>
   <h3>Пример 1</h3>
   <table class="sample-tests">
      <thead>
         <tr>
            <th>Ввод</th>
            <th>Вывод</th>
         </tr>
      </thead>
      <tbody>
         <tr>
            <td><pre>5
1 9 4 2 3
3
</pre></td>
            <td><pre>2
3
</pre></td>
         </tr>
      </tbody>
   </table>
   <h3>Пример 2</h3>
   <table class="sample-tests">
      <thead>
         <tr>
            <th>Ввод</th>
            <th>Вывод</th>
         </tr>
      </thead>
      <tbody>
         <tr>
            <td><pre>0

0
</pre></td>
            <td><pre>0
0
</pre></td>
         </tr>
      </tbody>
   </table>
   <h3>Пример 3</h3>
   <table class="sample-tests">
      <thead>
         <tr>
            <th>Ввод</th>
            <th>Вывод</th>
         </tr>
      </thead>
      <tbody>
         <tr>
            <td><pre>1
0
0
</pre></td>
            <td><pre>0
1
</pre></td>
         </tr>
      </tbody>
   </table>
   <h2>Примечания</h2>
   <div class="notes"><p>Чтобы решить советуем реализовать функцию, которая принимает на вход предикат и пару итераторов, задающих массив (или массив
      и два индекса в нём), а возвращает точку разбиения, то есть итератор (индекс) на конец части, которая содержащит элементы,
      удовлетворяющие заданному предикату.</p>
      <p>В таком виде вам будет удобно использовать эту функцию для реализации сортировки.</p>
   </div>
</div>
"""
# https://api.contest.yandex.net/api/public/v2/contests/53029/submissions/141720838
submission_info = {
    'runId': 141720838,
    'authorId': 108927215,
    'submissionTime': '2025-09-02T14:08:17.000+03:00',
    'timeFromStart': 57956897869,
    'compiler': 'pypy3_7_1_0',
    'problemId': '4105/2015_01_14/BJQFReu5iY',
    'problemAlias': 'A',
    'source': "\r\n#ok\r\ndef partition(arr, x):\r\n    n = len(arr)\r\n    l, r = 0, n - 1\r\n    while r >= l:\r\n        while l < n and arr[l] < x:\r\n            l += 1\r\n        while r >= 0 and arr[r] >= x:\r\n            r -= 1\r\n        if r > l:\r\n            arr[l], arr[r] = arr[r], arr[l]\r\n            l += 1\r\n            r -= 1\r\n    return l\r\n\r\n\r\ndef main():\r\n    n = int(input())\r\n    arr = list(map(int, input().split()))\r\n    x = int(input())\r\n    ans = partition(arr, x)\r\n    print(ans, n - ans, sep='\\n')\r\n\r\n\r\nif __name__ == '__main__':\r\n    main()",
    'diff': '--- 141714595\n+++ 141720838\n@@ -1,4 +1,5 @@\n+\r\n #ok\r\n def partition(arr, x):\r\n     n = len(arr)\r\n     l, r = 0, n - 1\r',
    'compileLog': '',
    'verdict': 'OK',
    'score': None,
    'maxTimeUsage': 361,
    'maxMemoryUsage': 206090240,
    'testNumber': 0
}
