"""Original interview practice adaptations with independently specified test answers."""
from textwrap import dedent
from problem_notes import source, explain
EXTRA = []
def problem(id, title, topic, diff, days, sig, statement, code, cases, notes, evidence=(), track='Coding fundamentals', relevance='Practice clear Python, edge cases, and trade-offs for AI/backend interviews.', cmp='exact'):
    fn = id.replace('-', '_')
    code = dedent(code).strip().replace('def solve(', f'def {fn}(')
    EXTRA.append(dict(id=id,title=title,topic=topic,diff=diff,days=days,fn=fn,sig=sig,
        statement=statement,ref=code,kind='func',tree=False,cmp=cmp,
        inputs=[args for args, expected in cases], expected=[expected for args, expected in cases],
        explanation=explain(notes),sources=[source(k) for k in evidence],
        evidence='Reported / adapted' if evidence else 'Profile practice',track=track,relevance=relevance))

problem('meeting-rooms','Meeting Rooms II','Intervals','Medium',[4], 'intervals',
 'Return the minimum rooms for meetings `[start,end)` with start < end. A meeting ending at t releases its room for a meeting starting at t. Input may be unsorted; empty input returns 0.',
 '''
 def solve(intervals):
     import heapq
     ends = []
     answer = 0
     for start, end in sorted(intervals):
         while ends and ends[0] <= start:
             heapq.heappop(ends)
         heapq.heappush(ends, end)
         answer = max(answer, len(ends))
     return answer
 ''', [(([[0,10],[2,4],[4,8]],),2),(([],),0),(([[1,2],[2,3]],),1),(([[1,5],[1,5],[1,5]],),3),(([[4,7]],),1)],
 ('Sort meetings by start and keep a heap of active end times. Remove all finished meetings before inserting the next. The largest active count is the required room count.', 'For [0,10), [2,4), [4,8), the last meeting reuses the room freed at 4. Peak overlap is 2.', 'O(n log n) time, O(n) space.', 'Use <= when releasing half-open intervals; using < incorrectly adds rooms for touching meetings.', 'Assign room IDs as well as counting rooms.'), ['amazon19'])

problem('min-tree-depth','Minimum Depth of a Binary Tree','BFS / trees','Easy',[8,10], 'values',
 'Given a level-order tree list with None for missing children, return the minimum number of nodes from root to a leaf. Empty input returns 0. Use the provided build_tree helper.',
 '''
 def solve(values):
     from collections import deque
     root = build_tree(values)
     if root is None:
         return 0
     queue = deque([(root, 1)])
     while queue:
         node, depth = queue.popleft()
         if node.left is None and node.right is None:
             return depth
         for child in (node.left, node.right):
             if child is not None:
                 queue.append((child, depth + 1))
 ''', [(([1,2,3,None,4],),2),(([],),0),(([1,None,2,None,3],),3),(([1],),1),(([1,2],),2)],
 ('BFS visits shorter paths before longer paths. The first node without either child is the nearest leaf.', 'In [1,2,3,null,4], node 3 is a leaf at depth 2 even though node 2 continues deeper.', 'O(n) time and space including tree construction.', 'A missing child is not a leaf. Taking min(0,nonzero) in a naive recurrence gives a wrong answer.', 'Compare BFS early exit with a corrected recursive solution.'), ['meta_infra'])

problem('vertical-order','Binary Tree Vertical Order','BFS / trees','Medium',[8,10], 'values',
 'Return tree values grouped by column, left to right. Root column is 0; left/right children shift by −1/+1. Within each column use BFS order, visiting left before right. Input is a level-order list; empty returns [].',
 '''
 def solve(values):
     from collections import defaultdict, deque
     root = build_tree(values)
     if root is None:
         return []
     columns = defaultdict(list)
     queue = deque([(root, 0)])
     while queue:
         node, col = queue.popleft()
         columns[col].append(node.val)
         if node.left: queue.append((node.left, col - 1))
         if node.right: queue.append((node.right, col + 1))
     return [columns[c] for c in sorted(columns)]
 ''', [(([3,9,20,None,None,15,7],),[[9],[3,15],[20],[7]]),(([],),[]),(([1],),[[1]]),(([1,2,3,4,5,6,7],),[[4],[2],[1,5,6],[3],[7]]),(([1,None,2],),[[1],[2]])],
 ('Carry a horizontal column index through BFS and append each node to that column. Sorting only the column keys gives the left-to-right result.', 'In the full tree [1,2,3,4,5,6,7], nodes 1,5,6 share column 0 and occur in that order.', 'O(n+c log c) time and O(n) space for c columns.', 'Do not sort values within a column; this contract preserves BFS ties.', 'How does the rule differ from vertical traversal that sorts equal-row values?'), ['meta_infra'])

problem('restore-ip','Restore IPv4 Addresses','Backtracking','Medium',[15], 'digits',
 'From a string of ASCII digits, return all IPv4 addresses formed by inserting three dots. Each of four parts is 0–255, with no leading zeros except "0". Return addresses lexicographically sorted.',
 '''
 def solve(digits):
     out = []
     def visit(pos, parts):
         remaining = 4 - len(parts)
         if not remaining <= len(digits) - pos <= 3 * remaining:
             return
         if remaining == 0:
             out.append(".".join(parts))
             return
         for length in (1, 2, 3):
             part = digits[pos:pos + length]
             if len(part) != length: break
             if length > 1 and part[0] == "0": break
             if int(part) <= 255:
                 visit(pos + length, parts + [part])
     visit(0, [])
     return sorted(out)
 ''', [(("25525511135",),["255.255.11.135","255.255.111.35"]),(("0000",),["0.0.0.0"]),(("1111",),["1.1.1.1"]),(("123",),[]),(("999999999999",),[])],
 ('Choose 1–3 digits for each part and reject invalid parts immediately. The remaining characters must fit the remaining part count.', '0000 has exactly four single zero parts. Taking 00 is invalid even though its numeric value is zero.', 'Constant bounded search (at most 3⁴ branches) for four IPv4 parts; output storage is bounded.', 'Checking only int(part) misses leading zeros.', 'Write three nested split loops and compare readability and pruning.'), ['meta_infra'])

problem('nested-weight','Nested List Depth Sum','DFS','Easy',[8], 'items',
 'Input contains integers and nested lists. Top-level integers have weight 1, the next level weight 2, and so on. Return the weighted sum. Empty lists contribute zero.',
 '''
 def solve(items):
     def total(xs, depth):
         return sum(x * depth if isinstance(x, int) else total(x, depth + 1) for x in xs)
     return total(items, 1)
 ''', [(([1,[2,[3]]],),14),(([],),0),(([[1,1],2,[1,1]],),10),(([-2,[3]],),4),(([[],[[]]],),0)],
 ('Carry depth through recursion. Multiply only integer leaves; visiting a nested list increments depth but adds no value itself.', '[1,[2,[3]]] contributes 1×1 + 2×2 + 3×3 = 14.', 'O(N) time for all entries, O(depth) stack space.', 'A top-level integer starts at depth 1, not 0.', 'Invert the weights so shallower integers receive greater weight.'), ['meta_ml'])

problem('merge-unique','Merge Sorted Arrays Without Duplicates','Heap','Medium',[13], 'arrays',
 'Merge k nondecreasing integer arrays into one increasing array without duplicates. Empty arrays are allowed. This generalizes a reported three-array interview variant.',
 '''
 def solve(arrays):
     import heapq
     result = []
     for value in heapq.merge(*arrays):
         if not result or result[-1] != value:
             result.append(value)
     return result
 ''', [(([[1,2,2],[2,3],[1,4]],),[1,2,3,4]),(([],),[]),(([[],[]],),[]),(([[0,0],[0]],),[0]),(([[-3,-1],[-2,-1]],),[-3,-2,-1])],
 ('Merge the ordered streams with a heap. Equal values become adjacent, so compare each emitted value only with the last retained value.', '[1,2,2], [2,3], [1,4] emits 1,1,2,2,2,3,4; keeping changes gives 1,2,3,4.', 'O(N log k) time, O(k) auxiliary space plus unique output.', 'A set followed by sorting works but loses the advantage of already sorted input.', 'Use pairwise merges for exactly three arrays and compare auxiliary memory.'), ['meta_ml'])

problem('logger-cooldown','Logger Message Cooldown','Hash map','Easy',[1,24], 'events, cooldown',
 'Process `[timestamp,message]` events in nondecreasing time order. Accept a message if it has never been accepted or at least cooldown seconds have passed since its last accepted event. Return a Boolean per event. cooldown is positive; rejected events do not reset the timer.',
 '''
 def solve(events, cooldown):
     last = {}
     result = []
     for now, message in events:
         accept = message not in last or now - last[message] >= cooldown
         result.append(accept)
         if accept: last[message] = now
     return result
 ''', [(([[0,'a'],[4,'a'],[10,'a']],10),[True,False,True]),(([],10),[]),(([[1,'a'],[1,'b'],[1,'a']],1),[True,True,False]),(([[0,'a'],[9,'a'],[10,'a']],10),[True,False,True]),(([[0,'a'],[1,'a']],1),[True,True])],
 ('Remember the last accepted timestamp for each message. A rejected message changes no state, so repeated rejections cannot postpone its next valid time.', 'Accept a at 0, reject at 9, accept at 10 with a ten-second cooldown.', 'O(n) expected time, O(u) space for unique messages.', 'Updating timestamps on rejection changes the problem into a sliding inactivity timeout.', 'Bound memory with expiration and discuss out-of-order events.'), ['google_ml'],track='Practical backend',relevance='Useful for suppressing repeated ingestion errors and noisy LLM-service logs.')

problem('recipe-dependencies','Resolve Recipe Dependencies','Graphs','Medium',[11], 'recipes, ingredients, supplies',
 'recipes contains unique names, ingredients contains one list of required names per recipe, and supplies contains initially available names. Supplies are unlimited. Recipes may depend on other recipes and may have no ingredients. Return all buildable recipes sorted; unavailable cycles stay unbuilt.',
 '''
 def solve(recipes, ingredients, supplies):
     from collections import defaultdict, deque
     dependents = defaultdict(list)
     remaining = {}
     available = set(supplies)
     for recipe, needs in zip(recipes, ingredients):
         missing = set(needs) - available
         remaining[recipe] = len(missing)
         for item in missing: dependents[item].append(recipe)
     queue = deque(r for r in recipes if remaining[r] == 0 or r in available)
     emitted = set()
     while queue:
         item = queue.popleft()
         if item in emitted: continue
         emitted.add(item)
         for dependent in dependents[item]:
             remaining[dependent] -= 1
             if remaining[dependent] == 0: queue.append(dependent)
     return sorted(emitted)
 ''', [((['bread','sandwich'],[['flour'],['bread','ham']],['flour','ham']),['bread','sandwich']),((['a','b'],[['b'],['a']],[]),[]),((['a'],[[]],[]),['a']),((['a'],[['x']],[]),[]),(([],[],[]),[])],
 ('Count missing requirements and connect each ingredient to recipes waiting for it. A recipe becomes available when its missing count reaches zero, releasing other recipes.', 'Flour releases bread; bread plus existing ham releases sandwich. A cycle with no available entry point never enters the queue.', 'O(V+E+V log V) time including result sorting; O(V+E) space.', 'A missing raw ingredient is not a recipe you can magically produce. Count unique requirements once.', 'Apply this to an AI workflow DAG and report why blocked tasks cannot run.'), ['google_recipe'])

problem('sparse-matvec','Sparse Matrix–Vector Product','Sparse linear algebra','Medium',[9,23], 'rows, cols, entries, vector',
 'A rows×cols matrix is represented as `[row,column,value]` entries. Coordinates may repeat and their values add. Return A×vector as a dense list. Coordinates are valid and len(vector)=cols; omitted cells are zero.',
 '''
 def solve(rows, cols, entries, vector):
     out = [0] * rows
     for row, col, value in entries:
         out[row] += value * vector[col]
     return out
 ''', [((2,3,[[0,0,2],[1,2,4]],[3,0,5]),[6,20]),((2,2,[],[1,2]),[0,0]),((1,1,[[0,0,2],[0,0,3]],[4]),[20]),((0,0,[],[]),[]),((1,2,[[0,1,-2]],[9,3]),[-6])],
 ('Only stored entries can contribute. Multiply each by the matching vector coordinate and accumulate into its output row.', 'Entry [1,2,4] with vector[2]=5 contributes 20 to output row 1. No dense matrix needs to be allocated.', 'O(rows+nnz) time, O(rows) output space.', 'Repeated coordinates contribute more than once; assignment would lose their sum.', 'Build CSR row offsets for repeated matrix–vector multiplication.'), ['db_sparse'],track='AI / ML implementation',relevance='Connects to sparse text features, embeddings, and your NLP/data-engineering experience.')

problem('lazy-map','Lazy Chained Transform Search','Lazy evaluation','Medium',[24,25], 'values, operations, target',
 'operations is a list of `[multiplier,offset]` transformations x → multiplier*x+offset, applied in order. Return the first input index whose transformed value equals target, or −1. Evaluate elements lazily and stop at the first match. This is a serializable adaptation of a chained-map interview task.',
 '''
 def solve(values, operations, target):
     for index, value in enumerate(values):
         for multiplier, offset in operations:
             value = multiplier * value + offset
         if value == target:
             return index
     return -1
 ''', [(([1,2,3],[[2,0],[1,1]],5),1),(([],[],2),-1),(([1,2],[],2),1),(([1,2],[[0,3]],3),0),(([1,2],[[2,1]],10),-1)],
 ('Keep transformations as instructions. When searching, apply the chain to one element at a time and return as soon as it matches.', '[1,2,3] with ×2 then +1 yields 3 for index 0 and 5 for index 1; index 2 need not be evaluated.', 'O(nm) worst-case time for n values and m maps, O(1) auxiliary space.', 'Reversing operation order changes the result. Tests check values; explaining laziness also requires discussing evaluation count.', 'Support arbitrary callables and persistent chainable objects; consider composing affine maps once.'), ['db_lazy'],track='Practical backend',relevance='Relates to lazy ETL execution in Spark and composable Python processing.')

problem('hit-counter','Rolling Hit Counter','Sliding window','Medium',[3,24], 'events, window',
 'Process `[operation,timestamp]` events in nondecreasing timestamp order; operation is "hit" or "count". A count at t includes hits in (t−window,t]. Return one result per event: None for hit, integer for count. window>0.',
 '''
 def solve(events, window):
     from collections import deque
     hits = deque()
     out = []
     for op, now in events:
         while hits and hits[0] <= now - window:
             hits.popleft()
         if op == "hit":
             hits.append(now)
             out.append(None)
         else:
             out.append(len(hits))
     return out
 ''', [(([['hit',1],['hit',2],['count',3],['count',6]],5),[None,None,2,1]),(([['count',0]],3),[0]),(([['hit',0],['hit',0],['count',0]],1),[None,None,2]),(([['hit',0],['count',5]],5),[None,0]),(([],5),[])],
 ('A deque keeps timestamps in order. Remove expired hits from its front, append new hits at the back, and use its length for counts.', 'At t=6 with window 5, time 1 is excluded and time 2 remains. The left endpoint is open.', 'O(n) total time, O(active hits) state plus output.', 'Multiple hits at the same timestamp count separately.', 'Aggregate per-second counts or use a circular buffer; discuss timestamp precision.'), ['db_counter'],track='Practical backend',relevance='Measure recent request traffic and error rates for AI services.')

problem('bounded-crawler','Depth-Limited Graph Crawler','BFS','Medium',[10,25], 'links, start, max_depth',
 'links maps page IDs to lists of outgoing page IDs. Return sorted IDs reachable within max_depth edges from start, including start. Missing pages have no links; max_depth≥0. This offline graph adaptation performs no network requests.',
 '''
 def solve(links, start, max_depth):
     from collections import deque
     seen = {start}
     queue = deque([(start, 0)])
     while queue:
         page, depth = queue.popleft()
         if depth == max_depth: continue
         for neighbor in links.get(page, []):
             if neighbor not in seen:
                 seen.add(neighbor)
                 queue.append((neighbor, depth + 1))
     return sorted(seen)
 ''', [(({'a':['b'],'b':['a','c']},'a',1),['a','b']),(({'a':['b'],'b':['c']},'a',2),['a','b','c']),(({},'x',0),['x']),(({'a':['a','b','b']},'a',4),['a','b']),(({'a':['b']},'a',0),['a'])],
 ('BFS discovers each page at its shortest distance. Mark pages when enqueuing so cycles and duplicate links do not create repeated work.', 'At depth limit 1, a→b→c returns a and b; c is two edges away.', 'O(V+E+V log V) time including output sorting, O(V) space over visited pages.', 'DFS with one visited set can first discover a page by a longer path and miss reachable descendants under the depth budget.', 'Add bounded asynchronous fetching, same-host rules, retries, and cancellation.'), ['db_lazy'],track='Practical backend',relevance='Mirrors controlled traversal during document or codebase ingestion.')

problem('resumable-iterator','Resumable Iterator','State / APIs','Medium',[24,25], 'values, operations',
 'Simulate an iterator over values. Operations: ["next"] returns the next item, or None at exhaustion; ["save"] returns the current cursor; ["restore",cursor] restores a previously valid position and returns None. Return all operation results. Cursors are integers 0..len(values).',
 '''
 def solve(values, operations):
     cursor = 0
     out = []
     for op in operations:
         if op[0] == "next":
             if cursor == len(values):
                 out.append(None)
             else:
                 out.append(values[cursor])
                 cursor += 1
         elif op[0] == "save":
             out.append(cursor)
         else:
             cursor = op[1]
             out.append(None)
     return out
 ''', [(([10,20],[['next'],['save'],['next'],['restore',1],['next']]),[10,1,20,None,20]),(([],[['next'],['save']]),[None,0]),(([1],[['next'],['next'],['next'],['save']]),[1,None,None,1]),(([1,2],[['restore',2],['next']]),[None,None]),(([1],[['save'],['next'],['restore',0],['next']]),[0,1,None,1])],
 ('The state is the index of the next unread value. Saving copies that index; restoring changes the cursor without changing the underlying data.', 'After reading 10 from [10,20], cursor 1 is saved. Restoring 1 makes the next call return 20 again.', 'O(1) per operation; O(1) cursor state plus output.', 'Saving the last-read index causes off-by-one replay errors. Exhaustion must not advance beyond the end.', 'Support nested iterators and serialize state with a dataset version.'), ['openai'],track='Practical backend',relevance='Checkpoint ingestion or training pipelines so interrupted work can resume.')

problem('mini-database','In-Memory Filter and Order','Data processing','Medium',[24], 'rows, filters, order_key',
 'rows is a list of flat dictionaries. Keep rows containing every key/value pair in filters. Sort matching rows by order_key ascending (stable on ties) and return their id values. Every row has id and order_key; values for the ordering field are mutually comparable. Empty filters match everything.',
 '''
 def solve(rows, filters, order_key):
     matches = [row for row in rows
                if all(key in row and row[key] == value for key, value in filters.items())]
     return [row["id"] for row in sorted(matches, key=lambda row: row[order_key])]
 ''', [(([{'id':1,'x':3},{'id':2,'x':1}],{},'x'),[2,1]),(([{'id':1,'x':3},{'id':2,'x':1}],{'x':3},'x'),[1]),(([],{},'id'),[]),(([{'id':1},{'id':2,'x':None}],{'x':None},'id'),[2]),(([{'id':2,'x':1},{'id':1,'x':1}],{},'x'),[2,1])],
 ('Treat filtering and ordering as separate stages. Check key existence before comparing values, then rely on stable sorting to preserve equal-key input order.', 'Rows with x values 3 and 1 return IDs [2,1] when sorting by x; filtering x=3 first returns only [1].', 'O(nf + m log m) time for f filters and m matches, O(m) space.', 'Missing fields are different from fields explicitly set to None.', 'Extend this local subset with inserts, tombstone deletion, indexes, and multiple sort fields.'), ['openai'],track='Practical backend',relevance='Builds the data manipulation and storage reasoning used by ingestion services.')

problem('ttl-lru','LRU Cache with Expiration','Caching','Hard',[24], 'capacity, ttl, operations',
 'Simulate capacity≥0 cache with positive ttl. Operations are ["put",time,key,value] and ["get",time,key], in nondecreasing time. A put expires at time+ttl; get returns −1 if missing/expired. Gets refresh recency but not expiration. Remove expired keys before capacity eviction. Return None for put and values for get.',
 '''
 def solve(capacity, ttl, operations):
     from collections import OrderedDict
     cache = OrderedDict()
     out = []
     for op in operations:
         action, now, key = op[:3]
         for old_key in list(cache):
             if cache[old_key][1] <= now:
                 del cache[old_key]
         if action == "put":
             cache[key] = (op[3], now + ttl)
             cache.move_to_end(key)
             if len(cache) > capacity: cache.popitem(last=False)
             out.append(None)
         elif key in cache:
             cache.move_to_end(key)
             out.append(cache[key][0])
         else:
             out.append(-1)
     return out
 ''', [((2,5,[['put',0,'a',1],['get',4,'a'],['get',5,'a']]),[None,1,-1]),((1,10,[['put',0,'a',1],['put',1,'b',2],['get',2,'a']]),[None,None,-1]),((0,5,[['put',0,'a',1],['get',0,'a']]),[None,-1]),((1,5,[['put',0,'a',1],['put',4,'a',2],['get',5,'a']]),[None,None,2]),((2,5,[['put',0,'a',1],['put',1,'b',2],['get',2,'a'],['put',5,'c',3],['get',5,'b']]),[None,None,1,None,2])],
 ('Track recency and expiration independently. This teaching reference scans for expired entries before each operation, then uses OrderedDict for the LRU rule.', 'a inserted at 0 with TTL 5 expires exactly at 5, even if read at 4. A put at 4 instead resets its expiration to 9.', 'O(q·capacity) time for q operations due to expiration scans; O(capacity) state plus output.', 'The reference is intentionally not O(1): scanning avoids incorrectly evicting a live key while an expired key remains.', 'Use an expiry heap with version numbers and a linked-list LRU; discuss locking and stale heap entries.'), ['ms26'],track='Practical backend',relevance='Caching retrieved documents or model responses needs both freshness and recency.')

problem('word-abbreviation','Valid Word Abbreviation','Two pointers','Easy',[2], 'word, abbr',
 'word contains lowercase ASCII letters. abbr contains lowercase letters and ASCII digits. Digit runs skip that many word characters; zero and leading zeros are invalid. Return whether the abbreviation consumes the entire word.',
 '''
 def solve(word, abbr):
     i = j = 0
     while j < len(abbr):
         if abbr[j].isdigit():
             if abbr[j] == "0": return False
             count = 0
             while j < len(abbr) and abbr[j].isdigit():
                 count = count * 10 + int(abbr[j])
                 j += 1
             i += count
             if i > len(word): return False
         else:
             if i >= len(word) or word[i] != abbr[j]: return False
             i += 1
             j += 1
     return i == len(word)
 ''', [(('internationalization','i18n'),True),(('apple','a3e'),True),(('apple','a03e'),False),(('apple','6'),False),(('',''),True),(('a','0a'),False)],
 ('Walk the abbreviation while tracking a word cursor. Letters compare directly; a whole digit run advances the cursor once by its numeric value.', 'i18n matches the initial i, skips 18 middle letters, and matches the final n.', 'O(len(abbr)) time under ordinary integer-cost assumptions, O(1) state.', 'Matching a prefix is insufficient; both inputs must be completely consumed.', 'Add wildcard tokens and clarify ambiguity before coding.'), ['meta25'])

problem('fast-power','Power by Repeated Squaring','Binary arithmetic','Medium',[6], 'x, n',
 'Return x raised to integer n, including negative n. x is finite; x≠0 when n<0. Tests use finite outputs. Define x^0=1, including 0^0 for this exercise. Floating answers use tolerance 1e−6.',
 '''
 def solve(x, n):
     if n < 0:
         x, n = 1 / x, -n
     answer = 1.0
     while n:
         if n & 1: answer *= x
         x *= x
         n //= 2
     return answer
 ''', [((2,10),1024.0),((2,-3),0.125),((3,0),1.0),((-2,3),-8.0),((0,4),0.0)],
 ('Use the binary digits of the exponent. Multiply the answer for each set bit, square the base, and halve the exponent.', '2^5 uses bits 101: multiply by 2 and later by 16, producing 32.', 'O(log |n|) time, O(1) auxiliary space.', 'Invert the base for a negative exponent before the loop.', 'Discuss floating-point overflow and fixed-width integer minimum values.'), ['meta25'],cmp='approx')

problem('min-stack','Stack with Constant-Time Minimum','Stack','Medium',[12], 'operations',
 'Operations are ["push",value], ["pop"], ["top"], ["min"]. Return None for push, the removed value for pop, and the requested value for top/min. Non-push operations are only called on nonempty stacks.',
 '''
 def solve(operations):
     stack = []
     out = []
     for op in operations:
         if op[0] == "push":
             value = op[1]
             stack.append((value, min(value, stack[-1][1]) if stack else value))
             out.append(None)
         elif op[0] == "pop": out.append(stack.pop()[0])
         elif op[0] == "top": out.append(stack[-1][0])
         else: out.append(stack[-1][1])
     return out
 ''', [(([['push',3],['push',1],['min'],['pop'],['min']],),[None,None,1,1,3]),(([],),[]),(([['push',2],['push',2],['pop'],['min']],),[None,None,2,2]),(([['push',-1],['top']],),[None,-1]),(([['push',5],['push',6],['min']],),[None,None,5])],
 ('Each stack entry carries the minimum of the prefix ending there. Popping restores the previous prefix minimum automatically.', 'Push 3→(3,3), then 1→(1,1). Pop 1 and the minimum returns to 3.', 'O(1) per operation, O(n) stack space plus output.', 'A separate minimum stack must account for duplicate minima; storing a minimum per entry avoids that trap.', 'Support maximum and compare memory with a compressed minimum stack.'), ['ms25'])

problem('generate-parentheses','Generate Balanced Parentheses','Backtracking','Medium',[15], 'n',
 'Return lexicographically sorted strings with n matched pairs of parentheses, 0≤n≤9. For n=0 return [""].',
 '''
 def solve(n):
     result = []
     def visit(text, opened, closed):
         if closed == n:
             result.append(text)
             return
         if opened < n: visit(text + "(", opened + 1, closed)
         if closed < opened: visit(text + ")", opened, closed + 1)
     visit("", 0, 0)
     return result
 ''', [((0,),['']),((1,),['()']),((2,),['(())','()()']),((3,),['((()))','(()())','(())()','()(())','()()()'])],
 ('Never create an invalid prefix: add ( while fewer than n opens exist, and add ) only when an unmatched open exists. Choosing ( first gives lexical order.', 'At n=2, after (, either open again to produce (()) or close and reopen to produce ()().', 'O(n·Catalan(n)) time/output space; O(n²) peak auxiliary character storage with recursive string copies.', 'Generating all 2^(2n) strings and filtering wastes work on invalid prefixes.', 'Count solutions with DP without materializing them.'), ['ms25'])

problem('find-duplicate','Find Duplicate with Cycle Detection','Two pointers','Medium',[2], 'nums',
 'nums contains n+1 integers in 1..n, with exactly one distinct repeated value (possibly repeated more than twice). Return that value using O(1) auxiliary space and without modifying nums.',
 '''
 def solve(nums):
     slow = fast = nums[0]
     while True:
         slow = nums[slow]
         fast = nums[nums[fast]]
         if slow == fast: break
     slow = nums[0]
     while slow != fast:
         slow = nums[slow]
         fast = nums[fast]
     return slow
 ''', [(([1,3,4,2,2],),2),(([3,1,3,4,2],),3),(([1,1],),1),(([2,2,2,2,2],),2),(([1,2,3,4,4],),4)],
 ('Treat each value as a pointer to an index. The repeated target creates a cycle. Floyd’s slow/fast pointers meet inside it; resetting one to the start locates the cycle entrance.', '[1,3,4,2,2] follows 1→3→2→4→2; the repeated value 2 is the entrance.', 'O(n) time, O(1) space.', 'The 1..n value constraint is essential; arbitrary integers cannot safely be used as indices.', 'Explain the distance argument proving the reset phase reaches the entrance.'), ['ms25'])

problem('sparse-dot','Sparse Vector Dot Product','Sparse linear algebra','Easy',[9], 'a, b',
 'a and b map string coordinate IDs to numeric nonzero values. Missing coordinates mean zero. Return their dot product without building dense vectors.',
 '''
 def solve(a, b):
     if len(a) > len(b): a, b = b, a
     return sum(value * b.get(key, 0) for key, value in a.items())
 ''', [(({'0':2,'3':4},{'0':3,'2':9}),6),(({},{}),0),(({'x':-2},{'x':3}),-6),(({'a':1},{'b':2}),0),(({'a':2,'b':3},{'a':4,'b':5}),23)],
 ('Only shared coordinates contribute. Iterate the smaller dictionary and look up coordinates in the larger one.', 'a has 2 at coordinate 0 and b has 3 there, contributing 6. Unshared coordinates contribute zero.', 'Expected O(min(nnz(a),nnz(b))) time, O(1) space.', 'Do not zip dictionary values: their positions do not identify matching dimensions.', 'Use sorted coordinate arrays and a two-pointer merge.'),track='AI / ML implementation',relevance='Efficient similarity for sparse NLP features.')

problem('nearest-neighbors','Exact k-Nearest Embeddings','Vector retrieval','Medium',[9,14], 'query, vectors, k',
 'Return indices of the k nearest vectors by squared Euclidean distance, ties by smaller index. All vectors match query dimension; 0≤k≤len(vectors). Use plain Python.',
 '''
 def solve(query, vectors, k):
     ranked = []
     for index, vector in enumerate(vectors):
         distance = sum((a - b) ** 2 for a, b in zip(query, vector))
         ranked.append((distance, index))
     return [index for _, index in sorted(ranked)[:k]]
 ''', [(([0,0],[[1,0],[0,1],[3,3]],2),[0,1]),(([1],[[3],[1],[2]],1),[1]),(([],[[],[]],2),[0,1]),(([1],[],0),[]),(([0],[[1],[-1]],1),[0])],
 ('Compute squared distances; square roots are unnecessary because they preserve ordering. Sort distance/index pairs for deterministic ties.', 'From [0,0], [1,0] and [0,1] both have distance squared 1; index 0 wins the tie.', 'O(nd+n log n) time and O(n) space.', 'Do not confuse cosine and Euclidean rankings unless embeddings are appropriately normalized.', 'Replace full sorting with a size-k heap; discuss ANN recall versus latency.'),track='AI / ML implementation',relevance='An exact baseline for evaluating your Pinecone/Qdrant retrieval.')

problem('kmeans-step','One K-Means Update','ML algorithms','Medium',[23], 'points, centers',
 'Assign each point to its closest center by squared Euclidean distance, breaking ties by lower center index. Return the new mean centers; empty clusters keep their old center. centers is nonempty and all dimensions match.',
 '''
 def solve(points, centers):
     counts = [0] * len(centers)
     sums = [[0.0] * len(c) for c in centers]
     for point in points:
         index = min(range(len(centers)), key=lambda i: sum((x-y)**2 for x,y in zip(point, centers[i])))
         counts[index] += 1
         for j, value in enumerate(point): sums[index][j] += value
     return [[value / counts[i] for value in sums[i]] if counts[i] else list(centers[i])
             for i in range(len(centers))]
 ''', [(([[0],[2],[10]],[[0],[10]]),[[1.0],[10.0]]),(([],[[1,2]]),[[1,2]]),(([[2]],[[0],[4]]),[[2],[4]]),(([[0,0],[2,2]],[[0,0]]),[[1,1]]),(([[1]],[[1],[9]]),[[1],[9]])],
 ('Use the old centers for every assignment, accumulate sums/counts, then divide once. Keeping an empty center avoids division by zero.', 'Points 0 and 2 join center 0, whose new mean is 1. Point 10 keeps center 10 at 10.', 'O(nkd) time, O(kd) space.', 'Updating a center during assignment turns this into a different online algorithm.', 'Repeat until convergence; discuss initialization and empty-cluster reseeding.'),track='AI / ML implementation',relevance='Practice translating ML definitions into deterministic, testable code.',cmp='approx')

problem('linear-gradient','Linear Regression Gradient Step','ML algorithms','Medium',[24], 'X, y, weights, learning_rate',
 'Take one gradient step for mean squared error L=(1/n)Σ(Xw−y)², with no bias term. X is nonempty rectangular data, matching y and weights. Return updated weights. Compute the full batch gradient before updating.',
 '''
 def solve(X, y, weights, learning_rate):
     gradient = [0.0] * len(weights)
     for row, target in zip(X, y):
         error = sum(a*b for a,b in zip(row, weights)) - target
         for j, value in enumerate(row): gradient[j] += 2 * error * value / len(X)
     return [w - learning_rate*g for w,g in zip(weights, gradient)]
 ''', [(([[1],[2]],[2,4],[0],0.1),[1.0]),(([[1,0],[0,1]],[1,2],[0,0],0.1),[0.1,0.2]),(([[1]],[2],[2],0.1),[2]),(([[0]],[5],[3],0.2),[3]),(([[2]],[4],[0],0),[0])],
 ('Differentiate the squared error: each row contributes 2·error·feature/n. Sum all row contributions, then subtract learning_rate times the gradient.', 'X=[1,2], y=[2,4], w=0 gives gradient (−4−16)/2=−10. Learning rate 0.1 updates w to 1.', 'O(nd) time, O(d) space.', 'Updating a weight while still calculating the batch gradient mixes old and new model parameters.', 'Add bias, regularization, and finite-difference gradient checks.'),track='AI / ML implementation',relevance='Rehearse optimization mechanics behind your fine-tuning work.',cmp='approx')

problem('stable-sigmoid','Numerically Stable Sigmoid','AI fundamentals','Easy',[3], 'values',
 'Return sigmoid(x)=1/(1+exp(−x)) for each finite input value, avoiding overflow for large positive or negative inputs. Empty input returns [].',
 '''
 def solve(values):
     import math
     out = []
     for x in values:
         if x >= 0:
             out.append(1 / (1 + math.exp(-x)))
         else:
             e = math.exp(x)
             out.append(e / (1 + e))
     return out
 ''', [(([0],),[0.5]),(([1000,-1000],),[1,0]),(([],),[]),(([0,0],),[0.5,0.5]),(([1,-1],),[0.7310585786300049,0.2689414213699951])],
 ('Use algebraically equivalent formulas on either side of zero so the exponential’s argument is never positive.', 'For −1000, exp(−1000) underflows to zero, giving 0/(1+0)=0 without overflow.', 'O(n) time and output space.', 'The naive exp(−x) overflows for very negative x.', 'Explain sigmoid versus softmax for independent versus exclusive labels.'),track='AI / ML implementation',relevance='Reliable classifier probabilities and numerical debugging.',cmp='approx')

problem('binary-log-loss','Binary Cross-Entropy from Logits','AI fundamentals','Medium',[21,24], 'logits, labels',
 'Return mean binary cross-entropy from finite logits and 0/1 labels of equal nonzero length. Use the stable per-item formula max(z,0)−z*y+log(1+exp(−abs(z))).',
 '''
 def solve(logits, labels):
     import math
     return sum(max(z, 0) - z*y + math.log1p(math.exp(-abs(z)))
                for z,y in zip(logits, labels)) / len(logits)
 ''', [(([0,0],[0,1]),0.6931471805599453),(([1000,-1000],[1,0]),0.0),(([1000],[0]),1000.0),(([-1000],[1]),1000.0),(([0],[1]),0.6931471805599453)],
 ('Combine sigmoid and log loss algebraically. This avoids constructing probabilities that round to exactly zero or one before taking logarithms.', 'A logit of 0 predicts 0.5 and has loss log(2). A confident incorrect logit 1000 with label 0 has loss about 1000.', 'O(n) time, O(1) auxiliary space.', 'Clipping probabilities changes extreme losses; working directly from logits preserves the objective.', 'Derive its gradient sigmoid(z)−y.'),track='AI / ML implementation',relevance='Understand training losses and stable evaluation.',cmp='approx')

problem('classification-metrics','Precision, Recall, and F1','Evaluation','Easy',[21], 'truth, predicted',
 'truth and predicted contain matching binary labels. Return [precision,recall,F1] for positive label 1. Any metric with a zero denominator is defined as 0. Empty input returns [0,0,0].',
 '''
 def solve(truth, predicted):
     tp = sum(a == b == 1 for a,b in zip(truth, predicted))
     fp = sum(a == 0 and b == 1 for a,b in zip(truth, predicted))
     fn = sum(a == 1 and b == 0 for a,b in zip(truth, predicted))
     precision = tp / (tp + fp) if tp + fp else 0.0
     recall = tp / (tp + fn) if tp + fn else 0.0
     f1 = 2*tp / (2*tp + fp + fn) if 2*tp + fp + fn else 0.0
     return [precision, recall, f1]
 ''', [(([1,1,0],[1,0,1]),[0.5,0.5,0.5]),(([0,0],[0,0]),[0,0,0]),(([],[]),[0,0,0]),(([1,1],[1,1]),[1,1,1]),(([1,0,0],[1,1,1]),[1/3,1,0.5])],
 ('Count true positives, false positives, and false negatives. Precision asks how many positive predictions were correct; recall asks how many real positives were found.', 'One true positive, one false positive, one false negative gives precision=recall=F1=0.5.', 'O(n) time, O(1) space.', 'Accuracy can hide a failed minority class. State the zero-denominator convention explicitly.', 'Sweep a probability threshold and discuss precision/recall trade-offs.'),track='AI / ML implementation',relevance='Evaluate extraction and intent classification beyond raw accuracy.',cmp='approx')

problem('confusion-matrix','Multiclass Confusion Matrix','Evaluation','Easy',[21], 'truth, predicted, classes',
 'Labels are integers 0..classes−1. Return a classes×classes count matrix where rows are true labels and columns are predicted labels. Input label arrays have equal length.',
 '''
 def solve(truth, predicted, classes):
     matrix = [[0] * classes for _ in range(classes)]
     for actual, guess in zip(truth, predicted): matrix[actual][guess] += 1
     return matrix
 ''', [(([0,1,1],[0,0,1],2),[[1,0],[1,1]]),(([],[],2),[[0,0],[0,0]]),(([0,0],[0,0],1),[[2]]),(([2],[0],3),[[0,0,0],[0,0,0],[1,0,0]]),(([],[],0),[])],
 ('Allocate independent row lists and increment the cell at [actual][prediction]. The diagonal counts correct predictions; off-diagonal cells identify specific confusions.', 'True class 1 predicted as 0 increments row 1, column 0, not the reverse.', 'O(n+C²) time and O(C²) space.', '[[0]*C]*C aliases rows. Use a list comprehension to create independent rows.', 'Compute per-class recall and normalized confusion matrices.'),track='AI / ML implementation',relevance='Debug reminder/note/clarification confusions in NoteEchoes.')

problem('recall-at-k','Retrieval Recall at k','RAG / retrieval','Easy',[14,21], 'ranking, relevant, k',
 'Return the fraction of unique relevant document IDs present in the first k ranking positions. Duplicate results never earn extra credit but consume positions. k≥0. If relevant is empty, return 0.',
 '''
 def solve(ranking, relevant, k):
     relevant = set(relevant)
     return len(set(ranking[:k]) & relevant) / len(relevant) if relevant else 0.0
 ''', [((['a','b','c'],['a','c'],2),0.5),((['a','a'],['a','b'],2),0.5),(([],['a'],3),0),((['a'],[],1),0),((['a'],['a'],0),0)],
 ('Intersect retrieved top-k IDs with the ground-truth set and divide by the ground-truth size. Deduplicate IDs before scoring credit.', 'Top two results a,b cover one of relevant {a,c}, so recall is 1/2.', 'O(k+r) time and space, bounded by actual ranking length, with r relevant IDs.', 'Dividing by k computes a precision-like metric, not recall.', 'Compare exact and approximate retrievers across k and latency budgets.'),track='AI / ML implementation',relevance='Measure whether RAG retrieves the evidence needed to answer.',cmp='approx')

problem('ndcg','Normalized Discounted Cumulative Gain','RAG / retrieval','Medium',[14,21], 'relevances, k',
 'relevances gives nonnegative integer relevance grades in returned ranking order. DCG@k=Σ(2^grade−1)/log2(rank+1), with rank starting at 1. The ideal ranking sorts this same candidate set descending. Return DCG/idealDCG, or 0 when idealDCG=0; k≥0.',
 '''
 def solve(relevances, k):
     import math
     def dcg(values):
         return sum((2**grade - 1) / math.log2(i + 2) for i,grade in enumerate(values[:k]))
     ideal = dcg(sorted(relevances, reverse=True))
     return dcg(relevances) / ideal if ideal else 0.0
 ''', [(([3,2,1],3),1.0),(([0,0],2),0.0),(([0,1],1),0.0),(([1,0],2),1.0),(([],3),0.0),(([0,1],2),0.6309297535714575)],
 ('Discount later positions because high-relevance evidence is more useful near the top. Normalize against the best ordering of the same candidates.', 'Grades [0,1] give gain 1 at rank 2: DCG=1/log2(3). Ideal [1,0] has DCG=1, so NDCG≈0.631.', 'O(n log n) time and O(n) space for ideal sorting.', 'This local metric normalizes over the supplied candidate set; corpus-level evaluation needs complete ground truth.', 'Compare binary relevance with graded judgments and handle unjudged documents.'),track='AI / ML implementation',relevance='Assess reranking quality rather than only whether evidence was retrieved.',cmp='approx')

problem('overlap-chunks','Token Chunks with Overlap','RAG / ingestion','Easy',[14], 'tokens, size, overlap',
 'Split a token list into chunks of at most size tokens with overlap tokens shared between adjacent chunks. Require size>0 and 0≤overlap<size. Stop once a chunk reaches the end; do not emit a redundant trailing chunk. Empty input returns [].',
 '''
 def solve(tokens, size, overlap):
     chunks = []
     start = 0
     while start < len(tokens):
         chunks.append(tokens[start:start + size])
         if start + size >= len(tokens): break
         start += size - overlap
     return chunks
 ''', [(([1,2,3,4,5],3,1),[[1,2,3],[3,4,5]]),(([],3,1),[]),(([1,2],4,2),[[1,2]]),(([1,2,3,4],2,0),[[1,2],[3,4]]),(([1,2,3,4],3,2),[[1,2,3],[2,3,4]])],
 ('Advance by size−overlap, not by size. Once the current chunk includes the final token, stop immediately.', 'With size 3 and overlap 1, [1,2,3,4,5] becomes [1,2,3] and [3,4,5].', 'O(total emitted tokens) time and space; large overlap repeats more data.', 'A simple range loop can emit a redundant final chunk wholly contained in the previous chunk.', 'Attach source offsets and respect sentence boundaries and tokenizer units.'),track='AI / ML implementation',relevance='Directly supports document ingestion for enterprise RAG.')

problem('tfidf','Smoothed TF–IDF','NLP features','Medium',[14], 'documents',
 'documents is a list of already-tokenized string lists. Return one token→score dictionary per document. TF=count/token_count. IDF=log((1+number_of_documents)/(1+document_frequency))+1, using natural log. Empty documents return {}.',
 '''
 def solve(documents):
     import math
     from collections import Counter
     frequency = Counter(token for document in documents for token in set(document))
     result = []
     for document in documents:
         counts = Counter(document)
         result.append({token: count / len(document) * (math.log((1 + len(documents)) / (1 + frequency[token])) + 1)
                        for token, count in counts.items()})
     return result
 ''', [(([['a','a','b']],),[{'a':2/3,'b':1/3}]),(([[],[]],),[{},{}]),(([],),[]),(([['a'],['a']],),[{'a':1.0},{'a':1.0}]),(([['a'],[]],),[{'a':1.4054651081081644},{}])],
 ('Count how many documents contain each token, once per document. Multiply within-document frequency by a smoothed inverse document frequency.', 'A sole document [a,a,b] has IDF=1 for both terms, so scores are 2/3 and 1/3.', 'O(total tokens) expected time and O(vocabulary + output entries) space.', 'Document frequency is not total token frequency; repeating a word in one document counts once for IDF.', 'Normalize vectors and compare sparse retrieval with embedding retrieval.'),track='AI / ML implementation',relevance='Revisit the TF–IDF NLP pipelines listed on your résumé.',cmp='approx')

problem('attention','Single-Query Scaled Dot-Product Attention','AI fundamentals','Medium',[3,25], 'query, keys, values',
 'Compute softmax(query·key/sqrt(d)) over keys, then return the weighted sum of corresponding value vectors. query has dimension d>0; keys and values are nonempty matching lists with consistent dimensions. Use stable softmax.',
 '''
 def solve(query, keys, values):
     import math
     scores = [sum(a*b for a,b in zip(query, key)) / math.sqrt(len(query)) for key in keys]
     largest = max(scores)
     weights = [math.exp(score - largest) for score in scores]
     denominator = sum(weights)
     return [sum(weight * value[j] for weight,value in zip(weights, values)) / denominator
             for j in range(len(values[0]))]
 ''', [(([0],[[1],[2]],[[2,4],[4,8]]),[3,6]),(([1],[[1]],[[7,9]]),[7,9]),(([1000],[[1000],[1000]],[[1],[3]]),[2]),(([0,0],[[1,2],[3,4]],[[0],[10]]),[5]),(([0],[[1],[2]],[[0],[0]]),[0])],
 ('Compute query–key compatibility, scale by sqrt(d), normalize to probabilities, then combine value vectors. Subtract the maximum score before exponentiation.', 'A zero query gives equal scores for every key. Values [2,4] and [4,8] therefore average to [3,6].', 'O(n(d+v)) time, O(n+v) space for n keys and value dimension v.', 'Keys determine weights, but values supply the content being combined.', 'Add causal masks, multiple queries, and cached keys/values.'),track='AI / ML implementation',relevance='Make transformer attention concrete for LLM and vLLM discussions.',cmp='approx')

problem('layer-norm','Layer Normalization','AI fundamentals','Medium',[3], 'values, epsilon',
 'Normalize a nonempty vector using its mean and population variance: (x−mean)/sqrt(variance+epsilon). epsilon>0. No learned scale or bias in this exercise.',
 '''
 def solve(values, epsilon):
     import math
     mean = sum(values) / len(values)
     variance = sum((x - mean)**2 for x in values) / len(values)
     scale = math.sqrt(variance + epsilon)
     return [(x - mean) / scale for x in values]
 ''', [(([1,1],0.00001),[0,0]),(([2],1),[0]),(([0,2],3),[-0.5,0.5]),(([-2,2],12),[-0.5,0.5]),(([0,0,0],1),[0,0,0])],
 ('Normalize across the feature vector. A two-pass calculation finds the mean first and then squared deviations, avoiding subtraction of two large nearly equal moments.', '[0,2] has mean 1 and variance 1. With epsilon 3, the denominator is 2, giving [−0.5,0.5].', 'O(d) time and O(d) output space.', 'Use population variance (divide by d), not sample variance (d−1).', 'Add gamma/beta and compare LayerNorm with RMSNorm and BatchNorm.'),track='AI / ML implementation',relevance='Understand numerical operations inside transformer blocks.',cmp='approx')

problem('token-batches','Batch Requests under a Token Budget','LLM inference','Medium',[22], 'lengths, budget',
 'lengths contains request token counts in arrival order, each 1..budget. Group contiguous request indices greedily so each batch total is ≤budget. Preserve order; return lists of indices. This is an unpadded token-sum budget.',
 '''
 def solve(lengths, budget):
     result = []
     batch = []
     used = 0
     for index, length in enumerate(lengths):
         if used + length > budget:
             result.append(batch)
             batch, used = [], 0
         batch.append(index)
         used += length
     if batch: result.append(batch)
     return result
 ''', [(([3,4,2,5],7),[[0,1],[2,3]]),(([],5),[]),(([5,5],5),[[0],[1]]),(([1,2],9),[[0,1]]),(([4,4,1],5),[[0],[1,2]])],
 ('Keep a current batch and token sum. If the next request would exceed the budget, close the batch before inserting it.', 'Budget 7 admits lengths 3 and 4 together; the next batch takes 2 and 5.', 'O(n) time and O(n) output space.', 'Real padded batches may cost batch_size×max_length; the token-sum assumption must be explicit.', 'Add wait deadlines, padded costs, and fairness for long requests.'),track='AI / ML implementation',relevance='Relates to throughput, latency, and batching trade-offs in vLLM.')

problem('request-dedup','Deduplicate JSON Requests','Parsing / idempotency','Medium',[24], 'requests',
 'requests contains valid JSON strings of flat objects with string values. Return the index of the first equivalent request for every item. Whitespace and object-key order do not affect equivalence; string contents do. This adapts a reported request-replay task.',
 '''
 def solve(requests):
     import json
     first = {}
     out = []
     for index, request in enumerate(requests):
         obj = json.loads(request)
         key = tuple(sorted(obj.items()))
         if key not in first: first[key] = index
         out.append(first[key])
     return out
 ''', [((['{"a":"x","b":"y"}','{ "b": "y", "a": "x" }'],),[0,0]),(([],),[]),((['{}','{}'],),[0,0]),((['{"a":"x"}','{"a":"y"}'],),[0,1]),((['{"a":" x"}','{"a":"x"}','{"a":" x"}'],),[0,1,0])],
 ('Parse requests into objects and sort their key/value pairs to obtain a canonical immutable key. Remember the index of each first occurrence.', 'Objects {a:x,b:y} and {b:y,a:x} have the same canonical pairs despite different text ordering.', 'O(total text + Σ f log f) time for f fields per object; O(unique canonical data + output) space.', 'Removing whitespace from raw JSON can corrupt spaces inside string values.', 'Extend to nested JSON and discuss explicit idempotency keys, atomicity, and retry races.'), ['stripe'],track='Practical backend',relevance='Prevent duplicate work in ingestion and tool-execution APIs.')

problem('subscription-events','Subscription Reminder Schedule','Sorting / events','Medium',[4,24], 'subscriptions, offsets',
 'subscriptions contains [user,start,end] with integer days start≤end. Emit [start,user,"welcome"] and [end,user,"expired"]. For each unique positive offset d, emit [end−d,user,"reminder"] only if end−d≥start. Sort events by day, then user, then event name lexicographically. Return the schedule; no messages are sent.',
 '''
 def solve(subscriptions, offsets):
     events = []
     for user, start, end in subscriptions:
         events.extend([[start,user,"welcome"],[end,user,"expired"]])
         for offset in set(offsets):
             if end - offset >= start:
                 events.append([end - offset,user,"reminder"])
     return sorted(events)
 ''', [(([['a',0,10]],[3]),[[0,'a','welcome'],[7,'a','reminder'],[10,'a','expired']]),(([],[1]),[]),(([['a',0,2]],[3]),[[0,'a','welcome'],[2,'a','expired']]),(([['a',0,2]],[1,1]),[[0,'a','welcome'],[1,'a','reminder'],[2,'a','expired']]),(([['a',2,2]],[]),[[2,'a','expired'],[2,'a','welcome']])],
 ('Translate each subscription into independent dated events, discard reminders before the subscription begins, then sort with a fully specified tie rule.', 'A subscription from day 0 to 10 with offset 3 schedules its reminder at day 7.', 'O(S·D + E log E) time and O(E+D) space for S subscriptions, D offsets, and E emitted events.', 'Deduplicate offsets and state tie ordering, especially when start=end.', 'Add cancellations, plan changes, time zones, and rescheduling.'), ['stripe'],track='Practical backend',relevance='Practice deterministic event processing relevant to reminders and backend jobs.')

problem('token-bucket','Token Bucket Rate Limiter','Rate limiting','Medium',[22,24], 'times, capacity, refill_rate',
 'Given nondecreasing request times in seconds, return whether each request is accepted. Bucket starts full at time 0; capacity is a positive integer; refill_rate≥0 tokens/second. Each accepted request consumes one token. Refill continuously up to capacity. times are nonnegative.',
 '''
 def solve(times, capacity, refill_rate):
     tokens = float(capacity)
     last = 0
     out = []
     for now in times:
         tokens = min(capacity, tokens + (now - last) * refill_rate)
         accepted = tokens >= 1
         if accepted: tokens -= 1
         out.append(accepted)
         last = now
     return out
 ''', [(([0,0,0,1],2,1),[True,True,False,True]),(([],2,1),[]),(([0,100],1,0),[True,False]),(([0,0.5,1],1,1),[True,False,True]),(([0,10,10,10],2,1),[True,True,True,False])],
 ('Refill by elapsed time multiplied by rate, capped at capacity. Check and consume a token only after refilling.', 'Capacity 1 and rate 1: accept at 0; reject at 0.5 with half a token; accept at 1 after the remaining half refills.', 'O(n) time, O(1) state plus output.', 'Refill even after rejected calls, updating the timestamp so elapsed time is never counted twice.', 'Add per-tenant buckets and explain atomic updates across workers.'),track='Practical backend',relevance='Protect inference APIs and control bursty client traffic.')

problem('dense-rank','SQL-Style Dense Rank in Python','Data processing','Medium',[24], 'rows',
 'rows contains [group,score]. Return each row’s dense rank within its group, with higher scores first. Ties share a rank and the next distinct score increases rank by one. Preserve original row order.',
 '''
 def solve(rows):
     from collections import defaultdict
     scores = defaultdict(set)
     for group, score in rows: scores[group].add(score)
     ranks = {group: {score:i+1 for i,score in enumerate(sorted(values, reverse=True))}
              for group,values in scores.items()}
     return [ranks[group][score] for group,score in rows]
 ''', [(([['a',9],['a',9],['a',7],['b',1]],),[1,1,2,1]),(([],),[]),(([['a',1],['a',3],['a',2]],),[3,1,2]),(([['a',0],['b',0]],),[1,1]),(([['a',-1],['a',-2]],),[1,2])],
 ('Gather unique scores per group, sort them descending, and map each score to its one-based position. Look up ranks in original input order.', 'Scores 9,9,7 get 1,1,2. Ordinary RANK would instead give 1,1,3.', 'O(n + Σ u_g log u_g) time, O(n) space.', 'ROW_NUMBER, RANK, and DENSE_RANK have different tie behavior.', 'Write the equivalent SQL: DENSE_RANK() OVER (PARTITION BY group_name ORDER BY score DESC).'),track='Practical backend',relevance='Connects Python practice to your SQL and Spark data transformations.')

problem('bounded-async','Bounded Async Workers','Async Python','Medium',[25], 'values, limit',
 'Return the square of each integer in input order, using an async worker pool with at most limit tasks executing work concurrently (limit≥1). Simulate an awaitable operation with asyncio.sleep(0). Use async def; the test runner awaits your function. Functional tests check results; explain the concurrency bound separately.',
 '''
 async def solve(values, limit):
     import asyncio
     result = [None] * len(values)
     jobs = iter(enumerate(values))
     async def worker():
         for index, value in jobs:
             await asyncio.sleep(0)
             result[index] = value * value
     await asyncio.gather(*(worker() for _ in range(min(limit, len(values)))))
     return result
 ''', [(([3,1,2],2),[9,1,4]),(([],3),[]),(([-2,0],1),[4,0]),(([1,2],9),[1,4]),(([2,2,2],2),[4,4,4])],
 ('Create a fixed number of workers sharing a plain iterator. Taking the next job has no await, so one event-loop thread assigns each index exactly once. Store results by index to retain input order.', 'Two workers take indices 0 and 1; when one finishes it takes index 2. Completion order need not match output order.', 'O(n) work and O(n+limit) space; simulated yields do not parallelize CPU computation.', 'Creating one task per item with a semaphore bounds active work but still allocates n tasks. This version bounds task count too.', 'Add cancellation, per-item failures, real network I/O, and a queue for streaming input.'),track='Practical backend',relevance='Directly rehearses the asynchronous retrieval pipelines on your résumé.')
