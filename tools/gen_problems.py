"""Generates problems-data.js. Expected outputs come from the reference solutions below,
so test cases are never hand-typed. Run:  python3 tools/gen_problems.py"""
import json, copy, math, os

PRELUDE = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def build_tree(arr):
    """Level-order list (None = missing) -> TreeNode root."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0]); q = [root]; i = 1
    while q and i < len(arr):
        node = q.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i]); q.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i]); q.append(node.right)
        i += 1
    return root
'''

P = []
def add(id, title, topic, diff, days, statement, fn, sig, ref, inputs, cmp='exact', tree=False):
    P.append(dict(id=id, title=title, topic=topic, diff=diff, days=days, statement=statement,
                  fn=fn, sig=sig, ref=ref.strip('\n'), inputs=inputs, cmp=cmp, tree=tree, kind='func'))

def add_class(id, title, topic, diff, days, statement, cls, ref, inputs, starter):
    P.append(dict(id=id, title=title, topic=topic, diff=diff, days=days, statement=statement,
                  fn=cls, sig='', ref=ref.strip('\n'), inputs=inputs, cmp='exact', tree=False,
                  kind='class', starter=starter))

# ---------------- Arrays / hashing / pointers ----------------
add('two-sum', 'Two Sum', 'Hash map', 'Easy', [1],
 'Return the indices `[i, j]` (i < j) of the two numbers that add up to `target`. Exactly one solution exists.\n\nExample: `nums=[2,7,11,15], target=9` -> `[0,1]`',
 'two_sum', 'nums, target',
 'def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        if target - x in seen:\n            return [seen[target - x], i]\n        seen[x] = i',
 [([2,7,11,15],9),([3,2,4],6),([3,3],6),([-1,-2,-3,-4,-5],-8),([0,4,3,0],0),([1,5,9,13,17],22)])

add('three-sum', '3Sum', 'Two pointers', 'Medium', [2],
 'Return all unique triplets `[a,b,c]` with `a+b+c == 0`. Triplets may be in any order.\n\nExample: `[-1,0,1,2,-1,-4]` -> `[[-1,-1,2],[-1,0,1]]`',
 'three_sum', 'nums',
 'def three_sum(nums):\n    nums.sort(); res = []\n    for i in range(len(nums)-2):\n        if i and nums[i]==nums[i-1]: continue\n        l, r = i+1, len(nums)-1\n        while l < r:\n            s = nums[i]+nums[l]+nums[r]\n            if s < 0: l += 1\n            elif s > 0: r -= 1\n            else:\n                res.append([nums[i],nums[l],nums[r]]); l += 1\n                while l < r and nums[l]==nums[l-1]: l += 1\n    return res',
 [([-1,0,1,2,-1,-4],),([0,1,1],),([0,0,0],),([0,0,0,0],),([-2,0,1,1,2],),([],),([-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6],)], cmp='sorted2')

add('longest-substring', 'Longest Substring Without Repeating Characters', 'Sliding window', 'Medium', [3],
 'Return the length of the longest substring of `s` with no repeated characters.\n\nExample: `"abcabcbb"` -> `3`',
 'length_of_longest_substring', 's',
 'def length_of_longest_substring(s):\n    last = {}; best = start = 0\n    for i, c in enumerate(s):\n        if c in last and last[c] >= start: start = last[c] + 1\n        last[c] = i; best = max(best, i - start + 1)\n    return best',
 [("abcabcbb",),("bbbbb",),("pwwkew",),("",),(" ",),("dvdf",),("abba",)])

add('min-window', 'Minimum Window Substring', 'Sliding window', 'Hard', [3],
 'Return the smallest substring of `s` containing every character of `t` (with multiplicity). Return `""` if none exists.\n\nExample: `s="ADOBECODEBANC", t="ABC"` -> `"BANC"`',
 'min_window', 's, t',
 'def min_window(s, t):\n    from collections import Counter\n    need = Counter(t); missing = len(t); best = (0, 10**9); l = 0\n    for r, c in enumerate(s):\n        if need[c] > 0: missing -= 1\n        need[c] -= 1\n        if missing == 0:\n            while need[s[l]] < 0: need[s[l]] += 1; l += 1\n            if r - l < best[1] - best[0]: best = (l, r)\n            need[s[l]] += 1; missing += 1; l += 1\n    return "" if best[1] == 10**9 else s[best[0]:best[1]+1]',
 [("ADOBECODEBANC","ABC"),("a","a"),("a","aa"),("ab","b"),("aa","aa"),("cabwefgewcwaefgcf","cae")])

add('merge-intervals', 'Merge Intervals', 'Intervals', 'Medium', [4],
 'Merge all overlapping intervals and return the result sorted by start.\n\nExample: `[[1,3],[2,6],[8,10],[15,18]]` -> `[[1,6],[8,10],[15,18]]`',
 'merge', 'intervals',
 'def merge(intervals):\n    out = []\n    for s, e in sorted(intervals):\n        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)\n        else: out.append([s, e])\n    return out',
 [([[1,3],[2,6],[8,10],[15,18]],),([[1,4],[4,5]],),([[1,4],[0,4]],),([[1,4],[2,3]],),([],),([[5,6]],),([[2,3],[4,5],[6,7],[8,9],[1,10]],)])

add('kth-largest', 'Kth Largest Element in an Array', 'Heap', 'Medium', [5],
 'Return the k-th largest element (not the k-th distinct). Aim for O(n log k) with a heap.\n\nExample: `[3,2,1,5,6,4], k=2` -> `5`',
 'find_kth_largest', 'nums, k',
 'def find_kth_largest(nums, k):\n    import heapq\n    return heapq.nlargest(k, nums)[-1]',
 [([3,2,1,5,6,4],2),([3,2,3,1,2,4,5,5,6],4),([1],1),([7,7,7],2),([-1,-2,-3],3)])

add('top-k-frequent', 'Top K Frequent Elements', 'Heap / bucket', 'Medium', [5],
 'Return the `k` most frequent elements, in ascending order of value (so the answer is deterministic).\n\nExample: `[1,1,1,2,2,3], k=2` -> `[1,2]`',
 'top_k_frequent', 'nums, k',
 'def top_k_frequent(nums, k):\n    from collections import Counter\n    return sorted(x for x, _ in Counter(nums).most_common(k))',
 [([1,1,1,2,2,3],2),([1],1),([4,4,4,5,5,6,6,6,6],2),([-1,-1,2,2,2,3],1),([1,2,3,4],4)])

add('search-rotated', 'Search in Rotated Sorted Array', 'Binary search', 'Medium', [6],
 'A sorted array of distinct ints was rotated at an unknown pivot. Return the index of `target`, or -1. Must be O(log n).\n\nExample: `[4,5,6,7,0,1,2], target=0` -> `4`',
 'search', 'nums, target',
 'def search(nums, target):\n    l, r = 0, len(nums) - 1\n    while l <= r:\n        m = (l + r) // 2\n        if nums[m] == target: return m\n        if nums[l] <= nums[m]:\n            if nums[l] <= target < nums[m]: r = m - 1\n            else: l = m + 1\n        else:\n            if nums[m] < target <= nums[r]: l = m + 1\n            else: r = m - 1\n    return -1',
 [([4,5,6,7,0,1,2],0),([4,5,6,7,0,1,2],3),([1],0),([1],1),([3,1],1),([5,1,3],5),([6,7,8,1,2,3,4,5],8)])

add('max-subarray', 'Maximum Subarray (Kadane)', 'DP / arrays', 'Medium', [6,7],
 'Return the largest sum of any contiguous non-empty subarray.\n\nExample: `[-2,1,-3,4,-1,2,1,-5,4]` -> `6`',
 'max_sub_array', 'nums',
 'def max_sub_array(nums):\n    best = cur = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x); best = max(best, cur)\n    return best',
 [([-2,1,-3,4,-1,2,1,-5,4],),([1],),([5,4,-1,7,8],),([-3,-2,-1],),([0,0,0],)])

add('trapping-rain', 'Trapping Rain Water', 'Two pointers', 'Hard', [27,7],
 'Given `height[i]` bar heights (width 1), return how many units of water are trapped after raining.\n\nExample: `[0,1,0,2,1,0,1,3,2,1,2,1]` -> `6`',
 'trap', 'height',
 'def trap(height):\n    l, r = 0, len(height) - 1; lm = rm = water = 0\n    while l < r:\n        if height[l] < height[r]:\n            lm = max(lm, height[l]); water += lm - height[l]; l += 1\n        else:\n            rm = max(rm, height[r]); water += rm - height[r]; r -= 1\n    return water',
 [([0,1,0,2,1,0,1,3,2,1,2,1],),([4,2,0,3,2,5],),([],),([1],),([3,0,3],),([5,4,3,2,1],),([2,0,2],),([0,7,1,4,6],)])

add('container-water', 'Container With Most Water', 'Two pointers', 'Medium', [27],
 'Choose two lines to form a container with the x-axis; return the maximum water it can hold.\n\nExample: `[1,8,6,2,5,4,8,3,7]` -> `49`',
 'max_area', 'height',
 'def max_area(height):\n    l, r, best = 0, len(height) - 1, 0\n    while l < r:\n        best = max(best, min(height[l], height[r]) * (r - l))\n        if height[l] < height[r]: l += 1\n        else: r -= 1\n    return best',
 [([1,8,6,2,5,4,8,3,7],),([1,1],),([4,3,2,1,4],),([1,2,1],),([2,3,10,5,7,8,9],)])

add('product-except-self', 'Product of Array Except Self', 'Prefix / suffix', 'Medium', [17],
 'Return `out` where `out[i]` is the product of all elements except `nums[i]`. No division, O(n).\n\nExample: `[1,2,3,4]` -> `[24,12,8,6]`',
 'product_except_self', 'nums',
 'def product_except_self(nums):\n    n = len(nums); out = [1]*n; p = 1\n    for i in range(n): out[i] = p; p *= nums[i]\n    p = 1\n    for i in range(n-1, -1, -1): out[i] *= p; p *= nums[i]\n    return out',
 [([1,2,3,4],),([-1,1,0,-3,3],),([2,3],),([0,0],),([5,1,1,1],)])

add('subarray-sum-k', 'Subarray Sum Equals K', 'Prefix sum + hash map', 'Medium', [18],
 'Return the number of contiguous subarrays whose sum equals `k`.\n\nExample: `[1,1,1], k=2` -> `2`',
 'subarray_sum', 'nums, k',
 'def subarray_sum(nums, k):\n    cnt = {0: 1}; s = res = 0\n    for x in nums:\n        s += x; res += cnt.get(s - k, 0); cnt[s] = cnt.get(s, 0) + 1\n    return res',
 [([1,1,1],2),([1,2,3],3),([1],0),([1,-1,0],0),([3,4,7,2,-3,1,4,2],7)])

add('daily-temperatures', 'Daily Temperatures', 'Monotonic stack', 'Medium', [12],
 'For each day return how many days until a warmer temperature (0 if never).\n\nExample: `[73,74,75,71,69,72,76,73]` -> `[1,1,4,2,1,1,0,0]`',
 'daily_temperatures', 'temps',
 'def daily_temperatures(temps):\n    res = [0]*len(temps); st = []\n    for i, t in enumerate(temps):\n        while st and temps[st[-1]] < t:\n            j = st.pop(); res[j] = i - j\n        st.append(i)\n    return res',
 [([73,74,75,71,69,72,76,73],),([30,40,50,60],),([30,60,90],),([90,80,70],),([50],)])

add('valid-parentheses', 'Valid Parentheses', 'Stack', 'Easy', [12],
 'Given a string of `()[]{}` return True if brackets are balanced and correctly nested.\n\nExample: `"()[]{}"` -> `True`',
 'is_valid', 's',
 'def is_valid(s):\n    pairs = {")":"(", "]":"[", "}":"{"}; st = []\n    for c in s:\n        if c in pairs:\n            if not st or st.pop() != pairs[c]: return False\n        else: st.append(c)\n    return not st',
 [("()",),("()[]{}",),("(]",),("([)]",),("{[]}",),("",),("((",),("]",)])

add('decode-string', 'Decode String', 'Stack', 'Medium', [12],
 'Decode strings of the form `k[encoded]` (repeat `encoded` k times; nesting allowed).\n\nExample: `"3[a2[c]]"` -> `"accaccacc"`',
 'decode_string', 's',
 'def decode_string(s):\n    st = []; cur = ""; num = 0\n    for c in s:\n        if c.isdigit(): num = num*10 + int(c)\n        elif c == "[": st.append((cur, num)); cur, num = "", 0\n        elif c == "]":\n            prev, k = st.pop(); cur = prev + cur*k\n        else: cur += c\n    return cur',
 [("3[a]2[bc]",),("3[a2[c]]",),("2[abc]3[cd]ef",),("abc",),("10[a]",),("2[2[2[x]]]",)])

# ---------------- Trees / graphs ----------------
add('validate-bst', 'Validate Binary Search Tree', 'DFS / trees', 'Medium', [8],
 'Return True if the binary tree is a valid BST. The input is delivered as a `TreeNode` (fields `val`, `left`, `right`). The helpers `TreeNode` and `build_tree(level_order_list)` are available in the terminal for your own tests.\n\nExample: `[2,1,3]` -> `True`;  `[5,1,4,None,None,3,6]` -> `False`',
 'is_valid_bst', 'root',
 'def is_valid_bst(root):\n    def go(n, lo, hi):\n        if not n: return True\n        if not (lo < n.val < hi): return False\n        return go(n.left, lo, n.val) and go(n.right, n.val, hi)\n    return go(root, float("-inf"), float("inf"))',
 [([2,1,3],),([5,1,4,None,None,3,6],),([],),([1],),([2,2,2],),([5,4,6,None,None,3,7],),([10,5,15,None,None,6,20],)], tree=True)

add('max-depth', 'Maximum Depth of Binary Tree', 'DFS / trees', 'Easy', [8],
 'Return the maximum depth (number of nodes on the longest root-to-leaf path). Input is a `TreeNode`.\n\nExample: `[3,9,20,None,None,15,7]` -> `3`',
 'max_depth', 'root',
 'def max_depth(root):\n    return 0 if not root else 1 + max(max_depth(root.left), max_depth(root.right))',
 [([3,9,20,None,None,15,7],),([1,None,2],),([],),([1],),([1,2,3,4,None,None,5,6],)], tree=True)

add('num-islands', 'Number of Islands', 'DFS / grids', 'Medium', [9],
 'Grid of `"1"` (land) and `"0"` (water). Count 4-directionally connected islands.\n\nExample: `[["1","1","0"],["0","0","1"]]` -> `2`',
 'num_islands', 'grid',
 'def num_islands(grid):\n    g = [r[:] for r in grid]; n = 0\n    def sink(i, j):\n        if i<0 or j<0 or i>=len(g) or j>=len(g[0]) or g[i][j] != "1": return\n        g[i][j] = "0"\n        sink(i+1,j); sink(i-1,j); sink(i,j+1); sink(i,j-1)\n    for i in range(len(g)):\n        for j in range(len(g[0])):\n            if g[i][j] == "1": n += 1; sink(i, j)\n    return n',
 [([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]],),
  ([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]],),
  ([["0"]],),([["1"]],),([["1","0","1"],["0","1","0"],["1","0","1"]],)])

add('rotting-oranges', 'Rotting Oranges', 'BFS', 'Medium', [10],
 'Grid: 0 empty, 1 fresh, 2 rotten. Each minute rotten oranges rot 4-neighbours. Return minutes until none fresh, or -1 if impossible.\n\nExample: `[[2,1,1],[1,1,0],[0,1,1]]` -> `4`',
 'oranges_rotting', 'grid',
 'def oranges_rotting(grid):\n    from collections import deque\n    g = [r[:] for r in grid]; q = deque(); fresh = 0\n    for i in range(len(g)):\n        for j in range(len(g[0])):\n            if g[i][j] == 2: q.append((i,j))\n            elif g[i][j] == 1: fresh += 1\n    t = 0\n    while q and fresh:\n        for _ in range(len(q)):\n            i, j = q.popleft()\n            for a, b in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):\n                if 0<=a<len(g) and 0<=b<len(g[0]) and g[a][b]==1:\n                    g[a][b] = 2; fresh -= 1; q.append((a,b))\n        t += 1\n    return -1 if fresh else t',
 [([[2,1,1],[1,1,0],[0,1,1]],),([[2,1,1],[0,1,1],[1,0,1]],),([[0,2]],),([[0]],),([[1]],),([[2,2],[1,1],[0,0],[2,0]],)])

add('course-schedule', 'Course Schedule (Topological Sort)', 'Graphs', 'Medium', [11],
 'There are `n` courses; `prerequisites[i] = [a, b]` means take b before a. Return True if all courses can be finished (no cycle).\n\nExample: `n=2, [[1,0]]` -> `True`;  `n=2, [[1,0],[0,1]]` -> `False`',
 'can_finish', 'n, prerequisites',
 'def can_finish(n, prerequisites):\n    from collections import deque\n    adj = [[] for _ in range(n)]; indeg = [0]*n\n    for a, b in prerequisites: adj[b].append(a); indeg[a] += 1\n    q = deque(i for i in range(n) if indeg[i] == 0); seen = 0\n    while q:\n        u = q.popleft(); seen += 1\n        for v in adj[u]:\n            indeg[v] -= 1\n            if indeg[v] == 0: q.append(v)\n    return seen == n',
 [(2,[[1,0]]),(2,[[1,0],[0,1]]),(1,[]),(4,[[1,0],[2,1],[3,2]]),(4,[[1,0],[2,1],[3,2],[1,3]]),(3,[[0,1],[0,2],[1,2]])])

add('merge-k-sorted', 'Merge K Sorted Lists', 'Heap', 'Hard', [13],
 'Merge `k` sorted Python lists into one sorted list (use a heap for O(N log k)).\n\nExample: `[[1,4,5],[1,3,4],[2,6]]` -> `[1,1,2,3,4,4,5,6]`',
 'merge_k_sorted', 'lists',
 'def merge_k_sorted(lists):\n    import heapq\n    return list(heapq.merge(*lists))',
 [([[1,4,5],[1,3,4],[2,6]],),([],),([[]],),([[],[1]],),([[5],[1],[3]],),([[1,2,3],[4,5,6]],)])

# ---------------- Backtracking ----------------
add('subsets', 'Subsets', 'Backtracking', 'Medium', [15],
 'Return all subsets (the power set) of a list of unique integers. Any order; inner order does not matter.\n\nExample: `[1,2,3]` -> 8 subsets',
 'subsets', 'nums',
 'def subsets(nums):\n    res = [[]]\n    for x in nums: res += [s + [x] for s in res]\n    return res',
 [([1,2,3],),([0],),([],),([1,2],),([5,6,7,8],)], cmp='sorted2')

add('word-search', 'Word Search', 'Backtracking', 'Medium', [16],
 'Return True if `word` can be built from sequentially adjacent (4-dir) cells of `board`, each cell used at most once.',
 'exist', 'board, word',
 'def exist(board, word):\n    R, C = len(board), len(board[0])\n    def go(i, j, k):\n        if k == len(word): return True\n        if i<0 or j<0 or i>=R or j>=C or board[i][j] != word[k]: return False\n        t = board[i][j]; board[i][j] = "#"\n        ok = go(i+1,j,k+1) or go(i-1,j,k+1) or go(i,j+1,k+1) or go(i,j-1,k+1)\n        board[i][j] = t; return ok\n    return any(go(i,j,0) for i in range(R) for j in range(C))',
 [([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"ABCCED"),
  ([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"SEE"),
  ([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"ABCB"),
  ([["a"]],"a"),([["a","b"]],"ba"),([["a","a"]],"aaa")])

# ---------------- DP / greedy ----------------
add('unique-paths', 'Unique Paths', 'DP', 'Medium', [19],
 'Robot moves only right or down from top-left to bottom-right of an `m x n` grid. Count distinct paths.\n\nExample: `m=3, n=7` -> `28`',
 'unique_paths', 'm, n',
 'def unique_paths(m, n):\n    dp = [1]*n\n    for _ in range(1, m):\n        for j in range(1, n): dp[j] += dp[j-1]\n    return dp[-1]',
 [(3,7),(3,2),(1,1),(7,3),(10,10),(1,5)])

add('climb-stairs', 'Climbing Stairs', 'DP', 'Easy', [19],
 'You can climb 1 or 2 steps. In how many distinct ways can you climb `n` steps?\n\nExample: `n=3` -> `3`',
 'climb_stairs', 'n',
 'def climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n-1): a, b = b, a+b\n    return b',
 [(1,),(2,),(3,),(5,),(10,),(30,)])

add('house-robber', 'House Robber', 'DP', 'Medium', [19],
 'Rob houses in a line with values `nums`; you cannot rob two adjacent houses. Return the max total.\n\nExample: `[2,7,9,3,1]` -> `12`',
 'rob', 'nums',
 'def rob(nums):\n    a = b = 0\n    for x in nums: a, b = b, max(b, a + x)\n    return b',
 [([1,2,3,1],),([2,7,9,3,1],),([5],),([2,1,1,2],),([],),([10,1,1,10,1,1,10],)])

add('word-break', 'Word Break', 'DP', 'Medium', [20],
 'Return True if `s` can be segmented into a space-separated sequence of words from `wordDict`.\n\nExample: `"leetcode", ["leet","code"]` -> `True`',
 'word_break', 's, wordDict',
 'def word_break(s, wordDict):\n    w = set(wordDict); dp = [True] + [False]*len(s)\n    for i in range(1, len(s)+1):\n        dp[i] = any(dp[j] and s[j:i] in w for j in range(i))\n    return dp[-1]',
 [("leetcode",["leet","code"]),("applepenapple",["apple","pen"]),("catsandog",["cats","dog","sand","and","cat"]),("a",["b"]),("aaaaaaa",["aaaa","aaa"]),("",["a"])])

add('coin-change', 'Coin Change', 'DP', 'Medium', [20],
 'Return the fewest coins needed to make `amount`, or -1 if impossible. Unlimited coins of each type.\n\nExample: `coins=[1,2,5], amount=11` -> `3`',
 'coin_change', 'coins, amount',
 'def coin_change(coins, amount):\n    dp = [0] + [float("inf")]*amount\n    for a in range(1, amount+1):\n        for c in coins:\n            if c <= a: dp[a] = min(dp[a], dp[a-c] + 1)\n    return -1 if dp[amount] == float("inf") else dp[amount]',
 [([1,2,5],11),([2],3),([1],0),([186,419,83,408],6249),([2,5,10,1],27),([3,7],5)])

add('lis', 'Longest Increasing Subsequence', 'DP / binary search', 'Medium', [20],
 'Return the length of the longest strictly increasing subsequence. Try the O(n log n) patience-sorting approach.\n\nExample: `[10,9,2,5,3,7,101,18]` -> `4`',
 'length_of_lis', 'nums',
 'def length_of_lis(nums):\n    import bisect\n    t = []\n    for x in nums:\n        i = bisect.bisect_left(t, x)\n        if i == len(t): t.append(x)\n        else: t[i] = x\n    return len(t)',
 [([10,9,2,5,3,7,101,18],),([0,1,0,3,2,3],),([7,7,7,7],),([1],),([5,4,3,2,1],),([1,3,6,7,9,4,10,5,6],)])

add('jump-game', 'Jump Game', 'Greedy', 'Medium', [22],
 '`nums[i]` is the max jump length from index i. Return True if you can reach the last index from index 0.\n\nExample: `[2,3,1,1,4]` -> `True`',
 'can_jump', 'nums',
 'def can_jump(nums):\n    far = 0\n    for i, x in enumerate(nums):\n        if i > far: return False\n        far = max(far, i + x)\n    return True',
 [([2,3,1,1,4],),([3,2,1,0,4],),([0],),([0,1],),([2,0,0],),([1,1,1,1,0],)])

add('set-zeroes', 'Set Matrix Zeroes', 'Matrix', 'Medium', [23],
 'If an element is 0, set its entire row and column to 0. Return the resulting matrix (do not alter the shape).\n\nExample: `[[1,1,1],[1,0,1],[1,1,1]]` -> `[[1,0,1],[0,0,0],[1,0,1]]`',
 'set_zeroes', 'matrix',
 'def set_zeroes(matrix):\n    rows = {i for i,r in enumerate(matrix) if 0 in r}\n    cols = {j for r in matrix for j,v in enumerate(r) if v == 0}\n    return [[0 if i in rows or j in cols else v for j,v in enumerate(r)] for i,r in enumerate(matrix)]',
 [([[1,1,1],[1,0,1],[1,1,1]],),([[0,1,2,0],[3,4,5,2],[1,3,1,5]],),([[1]],),([[0]],),([[1,2],[3,4]],)])

# ---------------- AI-engineer coding rounds (tie to your resume) ----------------
add('softmax', 'Implement Softmax (numerically stable)', 'AI fundamentals', 'Easy', [3,25],
 'Return the softmax of a list of floats. Subtract the max first so `exp` does not overflow. Results are compared with tolerance 1e-6.\n\nExample: `[1,2,3]` -> `[0.0900, 0.2447, 0.6652]`',
 'softmax', 'xs',
 'def softmax(xs):\n    import math\n    m = max(xs); e = [math.exp(x - m) for x in xs]; s = sum(e)\n    return [v / s for v in e]',
 [([1,2,3],),([1000,1000],),([-1000,0],),([0],),([2.0,1.0,0.1],)], cmp='approx')

add('cosine-sim', 'Cosine Similarity', 'AI fundamentals', 'Easy', [9,14],
 'Return cosine similarity of two equal-length vectors (return 0.0 if either has zero norm). Compared with tolerance 1e-6.\n\nExample: `[1,0],[0,1]` -> `0.0`',
 'cosine_similarity', 'a, b',
 'def cosine_similarity(a, b):\n    import math\n    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))\n    if na == 0 or nb == 0: return 0.0\n    return sum(x*y for x, y in zip(a, b)) / (na * nb)',
 [([1,0],[0,1]),([1,2,3],[1,2,3]),([1,2],[-1,-2]),([0,0],[1,1]),([3,4],[4,3])], cmp='approx')

add('kv-cache', 'KV Cache Memory (whiteboard math)', 'LLM inference', 'Easy', [11,12],
 'Return KV-cache size in **bytes**: `2 * layers * kv_heads * head_dim * tokens * bytes_per_elem`.\n\nNoteEchoes Qwen 0.6B: 28 layers, 8 KV heads, head_dim 128, fp16 (2 bytes), 1024 tokens -> `117440512`',
 'kv_cache_bytes', 'layers, kv_heads, head_dim, tokens, bytes_per_elem=2',
 'def kv_cache_bytes(layers, kv_heads, head_dim, tokens, bytes_per_elem=2):\n    return 2 * layers * kv_heads * head_dim * tokens * bytes_per_elem',
 [(28,8,128,1024),(32,8,128,4096),(32,8,128,1),(28,8,128,1024,1),(80,8,128,8192)])

add('tokens-per-sec', 'Max Decode Tokens/sec (bandwidth bound)', 'LLM inference', 'Easy', [12],
 'At batch size 1, decode speed ~ memory bandwidth / model bytes. Given `params_b` (billions of params), `bits` per weight and `bandwidth_gbs`, return tokens/sec rounded to 1 decimal.\n\nExample: `0.6B, 8-bit, 50 GB/s` -> `83.3`',
 'max_tokens_per_sec', 'params_b, bits, bandwidth_gbs',
 'def max_tokens_per_sec(params_b, bits, bandwidth_gbs):\n    gb = params_b * bits / 8\n    return round(bandwidth_gbs / gb, 1)',
 [(0.6,8,50),(7,4,50),(8,16,2000),(70,4,400),(0.6,4,100)])

add('rrf', 'Reciprocal Rank Fusion', 'RAG / retrieval', 'Medium', [14,16,25],
 'Fuse several ranked doc-id lists: `score(d) = sum 1/(k + rank)` (rank starts at 1, default `k=60`). Return doc ids sorted by score desc, ties broken by id ascending.\n\nUsed in NoteEchoes hybrid retrieval (FTS5 + E5).',
 'rrf_fuse', 'rankings, k=60',
 'def rrf_fuse(rankings, k=60):\n    sc = {}\n    for r in rankings:\n        for i, d in enumerate(r, 1): sc[d] = sc.get(d, 0) + 1 / (k + i)\n    return [d for d, _ in sorted(sc.items(), key=lambda t: (-t[1], t[0]))]',
 [([["a","b","c"],["b","c","a"]],),([["x"]],),([["a","b"],["c","d"]],),([["a","b","c"],["c","b","a"],["b","a","c"]],),([],)])

add('rslora', 'LoRA vs rsLoRA scaling', 'Fine-tuning', 'Easy', [24],
 'Return the update scaling factor, rounded to 2 decimals: LoRA uses `alpha / r`; rsLoRA uses `alpha / sqrt(r)`. Parameter `rs` selects the variant.\n\nNoteEchoes: `r=32, alpha=64, rs=True` -> `11.31`',
 'lora_scale', 'r, alpha, rs=False',
 'def lora_scale(r, alpha, rs=False):\n    import math\n    return round(alpha / (math.sqrt(r) if rs else r), 2)',
 [(32,64,True),(32,64,False),(8,16,True),(8,16),(64,128,True),(128,256,False)])

# ---------------- class-design problems ----------------
add_class('lru-cache', 'LRU Cache', 'Design / hash map', 'Medium', [24],
 'Implement `LRUCache(capacity)` with `get(key)` (return -1 if absent) and `put(key, value)`. Both must be O(1); evict the least recently used key when full.',
 'LRUCache',
 'class LRUCache:\n    def __init__(self, capacity):\n        from collections import OrderedDict\n        self.c = OrderedDict(); self.cap = capacity\n    def get(self, key):\n        if key not in self.c: return -1\n        self.c.move_to_end(key); return self.c[key]\n    def put(self, key, value):\n        self.c[key] = value; self.c.move_to_end(key)\n        if len(self.c) > self.cap: self.c.popitem(last=False)',
 [dict(init=[2], ops=[["put",1,1],["put",2,2],["get",1],["put",3,3],["get",2],["put",4,4],["get",1],["get",3],["get",4]]),
  dict(init=[1], ops=[["put",2,1],["get",2],["put",3,2],["get",2],["get",3]]),
  dict(init=[2], ops=[["put",2,1],["put",2,2],["get",2],["put",1,1],["put",4,1],["get",2]]),
  dict(init=[3], ops=[["put",1,1],["put",2,2],["put",3,3],["get",1],["put",4,4],["get",2],["get",3],["get",4],["get",1]])],
 'class LRUCache:\n    def __init__(self, capacity):\n        pass\n\n    def get(self, key):\n        pass\n\n    def put(self, key, value):\n        pass\n')

add_class('trie', 'Implement Trie (Prefix Tree)', 'Design / trie', 'Medium', [26],
 'Implement `Trie` with `insert(word)`, `search(word)` (exact word) and `starts_with(prefix)`.',
 'Trie',
 'class Trie:\n    def __init__(self): self.root = {}\n    def insert(self, word):\n        n = self.root\n        for c in word: n = n.setdefault(c, {})\n        n["$"] = True\n    def search(self, word):\n        n = self.root\n        for c in word:\n            if c not in n: return False\n            n = n[c]\n        return "$" in n\n    def starts_with(self, prefix):\n        n = self.root\n        for c in prefix:\n            if c not in n: return False\n            n = n[c]\n        return True',
 [dict(init=[], ops=[["insert","apple"],["search","apple"],["search","app"],["starts_with","app"],["insert","app"],["search","app"]]),
  dict(init=[], ops=[["search","a"],["starts_with","a"],["insert","a"],["search","a"],["starts_with","a"]]),
  dict(init=[], ops=[["insert","note"],["insert","noteechoes"],["starts_with","notee"],["search","notee"],["search","noteechoes"]])],
 'class Trie:\n    def __init__(self):\n        pass\n\n    def insert(self, word):\n        pass\n\n    def search(self, word):\n        pass\n\n    def starts_with(self, prefix):\n        pass\n')


def run_ref(p):
    ns = {}
    exec(PRELUDE, ns)
    exec(p['ref'], ns)
    tests = []
    if p['kind'] == 'class':
        for t in p['inputs']:
            obj = ns[p['fn']](*t['init']); out = []
            for op in t['ops']:
                r = getattr(obj, op[0])(*op[1:])
                out.append(r)
            tests.append(dict(init=t['init'], ops=t['ops'], expected=out))
        return tests
    fn = ns[p['fn']]
    for args in p['inputs']:
        a = copy.deepcopy(list(args))
        if p['tree']:
            a[0] = ns['build_tree'](a[0])
        res = fn(*a)
        if isinstance(res, float) and not math.isfinite(res): raise ValueError(p['id'])
        tests.append(dict(args=list(args), expected=res))
    return tests

out = []
for p in P:
    tests = run_ref(p)
    starter = p.get('starter') or f"def {p['fn']}({p['sig']}):\n    # write your solution here\n    pass\n"
    out.append(dict(id=p['id'], title=p['title'], topic=p['topic'], diff=p['diff'], days=p['days'],
                    statement=p['statement'], fn=p['fn'], kind=p['kind'], cmp=p['cmp'], tree=p['tree'],
                    starter=starter, solution=p['ref'] + '\n', tests=tests))

here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(here, '..', 'problems-data.js')
with open(dest, 'w') as f:
    f.write('const PRELUDE_PY=' + json.dumps(PRELUDE) + ';\n')
    f.write('const PROBLEMS=' + json.dumps(out, separators=(',', ':')) + ';\n')
print(len(out), 'problems written to', os.path.abspath(dest))
