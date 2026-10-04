"""Handwritten explanations in nonblank source-line order after ast.unparse.
Each entry explains the operation in the context of this particular algorithm.
"""
LESSONS = {}
def notes(key, text):
    LESSONS[key] = [s.strip() for s in text.strip().split('\n') if s.strip()]
notes('two-sum', '''
Define the contract: accept numbers and a target, and return two distinct indices.
Create a value→index lookup so we can find a partner without rescanning earlier numbers.
Visit each number with its index; the index is required in the answer.
Ask whether the missing partner, target−x, has appeared before this position.
Return the earlier partner index and the current index; lookup-before-insert prevents reusing one element.
Remember this number for later positions. A future number may need it as its partner.
''')
notes('three-sum', '''
Accept the array and return unique value triplets summing to zero.
Sort values so moving a pointer predictably increases or decreases the sum.
Collect successful triplets here.
Choose an anchor, leaving at least two later positions for the other values.
Check whether this anchor repeats the preceding anchor, which would repeat answers.
Skip that repeated anchor and begin the next outer-loop iteration.
Place the other two pointers at opposite ends of the remaining suffix.
Continue only while the two pointers refer to distinct positions.
Compute the sum for this anchor and the current pair.
A negative sum means the current triplet is too small.
Move left inward to try a larger value.
A positive sum means the current triplet is too large.
Move right inward to try a smaller value.
The remaining case is exactly zero, so we have found a valid triplet.
Save its values, not its indices, as required by the contract.
Advance left to search for another pair for the same anchor.
While the new left value repeats the previous one, it would reproduce a triplet we already saved.
Skip that duplicate left value; checking l<r prevents crossing the pointers.
Return all unique triplets after every anchor has been considered.
''')
notes('longest-substring', '''
Accept a string and return the length of its longest repeat-free substring.
Map each character to its most recent position so repeats can be located immediately.
Start with an empty best length and a window beginning at index zero.
Scan rightward, keeping both the character and its position.
A repeated character matters only if its earlier occurrence is still inside this window.
Move the left boundary just past that occurrence, restoring a repeat-free window.
Record the current occurrence for future repetitions.
Compare the current inclusive window length i−start+1 with the best length so far.
Return the maximum length, not the final window length.
''')
notes('min-window', '''
Accept source s and required characters t; return the shortest covering substring.
Handle an empty target before trying to shrink a window.
No characters are required, so the minimum answer is empty.
Import a frequency table to track multiplicities, including repeated target letters.
Initialize each required character's count; positive means still needed, negative means surplus.
Count how many required occurrences remain unmatched, rather than only distinct letter types.
Use an impossibly large endpoint to represent that no valid answer exists yet.
Initialize the left boundary of the search window.
Expand the right boundary by one source character per iteration.
Check whether this occurrence fills an outstanding requirement.
One fewer required occurrence is now missing.
Account for the character even when it is surplus; negative counts enable later shrinking.
Only a fully covering window is eligible to become the answer.
Remove surplus characters at the left while coverage remains intact.
Restore that character's balance as it leaves the window.
Advance the left edge past the removed character.
Check whether this valid window is shorter than the best one saved so far.
Save both endpoints of the improved answer.
Remove one now-essential left character to make progress toward the next candidate.
The window is missing one required occurrence again.
Advance left; the outer loop will search for a replacement on the right.
Return empty if no window was found; otherwise slice through the saved right endpoint inclusively.
''')
notes('merge-intervals', '''
Accept intervals and return their merged union in start order.
Keep the already merged intervals here.
Sort by start so only the last saved interval can overlap the next one.
A nonempty result whose last end reaches this start means the intervals overlap or touch.
Extend the end only if necessary; max prevents a nested interval from shortening it.
Otherwise this interval begins a separate region.
Append a new two-element list so it can later be extended safely.
Return the merged intervals.
''')
notes('kth-largest', '''
Accept numbers and a one-based rank k; duplicate values count separately.
Import Python's heap operations and selection helpers.
Select the k largest values in descending order, then take the last: it is the smallest of those k, hence kth largest. nlargest maintains a bounded heap when useful and handles edge ranks specially.
''')
notes('top-k-frequent', '''
Accept values and the number of distinct values to select by frequency.
Import Counter to count each value's occurrences in one pass.
Count values, take the k highest-frequency (value,count) pairs, discard counts, then sort the selected values for the required output order. Equal frequency follows first encounter in Counter.
''')
notes('search-rotated', '''
Search a rotated array of distinct values and return the target index or −1.
Start with an inclusive search interval covering the entire array.
Continue while at least one candidate position remains.
Choose the midpoint using integer division.
Check the midpoint before discarding either half.
Return immediately when the target is found.
If left value≤middle value, the left half is sorted.
Check whether the target is inside that sorted half, excluding the already checked midpoint.
Keep only the positions left of the midpoint.
Otherwise the target cannot be in that sorted left half.
Keep only the positions right of the midpoint.
When the left half is not sorted, the right half is; test its target range.
Keep the sorted right half because it contains the target's possible value.
Otherwise discard that right half.
Move the inclusive right edge left of the midpoint.
No candidate remains, so the target is absent.
''')
notes('max-subarray', '''
Return the largest sum of a nonempty contiguous subarray.
Seed both totals with the first value so all-negative arrays are handled correctly.
Process remaining values; this slice creates a temporary list in Python.
Either start fresh at x or extend the best subarray ending one position earlier.
Keep the best total seen anywhere, not just the best ending here.
Return that global maximum.
''')
notes('trapping-rain', '''
Return the total water held between unit-width bars.
Place pointers at the outermost bars.
Start both running boundary heights and collected water at zero.
Work inward until no gap remains between pointers.
The lower current side can be resolved using its running maximum: an adequate opposite boundary already exists.
Update the highest left boundary seen before calculating the gap.
Add the gap between that boundary and this bar; the update ensures it is nonnegative.
This left position is finished, so move inward.
Otherwise resolve the right side using the symmetric argument.
Update the highest boundary encountered from the right.
Add water above this right bar.
Move inward after finishing this right position.
Return the accumulated water, including every resolved position exactly once.
''')
notes('container-water', '''
Return the greatest area obtainable from two selected boundary lines.
Start at maximum width and initialize the best area to zero.
Continue while there are two different boundary positions.
Compute width times the shorter height, and keep the best area found.
Identify whether the left boundary is the limiting height.
Discard it: retaining that height while decreasing width cannot improve its area.
Otherwise the right boundary is no taller than the left.
Discard that limiting right boundary instead.
Return the best area across all candidate pairs considered.
''')
notes('product-except-self', '''
Return the product of every other element at each position without division.
Record the output length.
Allocate one answer slot per element, initially the multiplicative identity 1.
Start the running left product at 1 because index zero has no left neighbors.
Visit positions from left to right.
Store the product strictly before the current index.
Include the current value for the next position's left product.
Reset the accumulator for products from the right.
Visit positions in reverse order.
Multiply the stored left product by the product strictly to this position's right.
Include the current value for the next reverse iteration.
Each slot now contains left product×right product, excluding its own element.
''')
notes('subarray-sum-k', '''
Count contiguous subarrays summing to k, including inputs with negative values.
Seed one empty prefix with sum zero so a subarray starting at index zero can be counted.
Start the running prefix sum and answer count at zero.
Add each next value to the current prefix.
Update the prefix total through the current position.
Every earlier prefix of s−k creates one valid subarray ending here; add its frequency.
Record this prefix only after counting matches, so an empty subarray cannot be counted.
Return the number of valid subarrays, not their contents.
''')
notes('daily-temperatures', '''
Return the number of days until a strictly warmer temperature at each position.
Default unanswered positions to zero, meaning no warmer day appears later.
Keep indices of days still waiting for a warmer temperature.
Visit each temperature with its index so distances can be calculated.
Resolve waiting days while today's temperature is strictly warmer than the stack top.
Remove the most recent unresolved day.
Today's index minus that day's index is its waiting time.
Push today as a new unresolved day; stack temperatures remain nonincreasing.
Return all waiting times, leaving unresolved entries at zero.
''')
notes('valid-parentheses', '''
Check that a bracket string is correctly nested and fully closed.
Map each closing bracket to the opener it requires.
Store unmatched opening brackets in last-in-first-out order.
Inspect every bracket in sequence.
Recognize a closing bracket by membership in the mapping.
Reject when there is no opener or the most recent opener has the wrong type; short-circuiting avoids popping an empty stack.
Return False immediately because no later bracket can repair this mismatch.
The other case is an opening bracket under the bracket-only input contract.
Remember it until its matching closer arrives.
Return True only if no unmatched openers remain.
''')
notes('decode-string', '''
Decode bracketed repetitions such as 2[a3[b]].
Keep outer text and repetition counts for nested blocks.
Start the current decoded block empty.
Accumulate the repetition count here.
Read one input character at a time.
Check whether this character extends a repetition count.
Shift previous digits by one decimal place and add the new digit, handling counts such as 12.
An opening bracket starts a nested block.
Save the current outer text and its pending repeat count.
Start the nested block with fresh text and a reset count.
A closing bracket finishes the nested block.
Recover its outer text and repeat count from the most recent saved state.
Repeat the completed inner text k times and attach it to the outer text.
Any other character is literal content.
Append the literal character to the current block.
Return the fully assembled text once every block is closed.
''')
notes('validate-bst', '''
Check the whole tree's ordering, not just parent–child comparisons.
Define a helper whose lo and hi are strict ancestor-imposed bounds.
An absent node contributes no ordering violation.
Return True for that empty subtree.
Reject a node at or outside either bound; duplicates are not allowed.
Return False as soon as the BST invariant is violated.
Narrow the upper bound on the left and the lower bound on the right; both subtrees must pass.
Start with unbounded limits so the root may hold any valid numeric value.
''')
notes('max-depth', '''
Return the number of nodes along the longest root-to-leaf path.
An empty tree has depth zero; otherwise recursively compute both child depths, keep the larger, and add the current node's one level.
''')
notes('num-islands', '''
Count four-direction connected components of string-valued land cells.
Copy every row so marking visited land does not modify the caller's grid.
Start the island count at zero.
Define flood fill from a candidate cell.
Stop when out of bounds or when the cell is water/already visited; short-circuit tests protect indexing.
Return from this unsuccessful branch without visiting neighbors.
Mark land as visited before recursing so cycles cannot revisit it.
Flood the neighbor below.
Flood the neighbor above.
Flood the neighbor to the right.
Flood the neighbor to the left.
Inspect each row for undiscovered land.
Inspect each column in that row.
An unvisited land cell starts a component not previously counted.
Count that new island exactly once.
Mark its entire component so later scan positions do not count it again.
Return the number of islands discovered.
''')
notes('rotting-oranges', '''
Find the minutes needed to rot all reachable fresh oranges, or −1 if some stay unreachable.
Import deque for constant-time removal from the front of a BFS queue.
Copy the grid because infection changes cell states.
Initialize the frontier of rotten oranges.
Track remaining fresh oranges to know when infection is complete.
Scan each grid row.
Scan its cells.
Find oranges that are already rotten at time zero.
Add all starting rotten cells to the same frontier, enabling simultaneous spread.
Identify fresh oranges separately.
Count them so a disconnected fresh region can be detected at the end.
No minutes have elapsed yet.
Process frontiers while there are infected cells to spread from and fresh cells left.
Freeze the frontier size for this minute so newly infected cells wait until the next minute.
Remove one rotten cell from the current frontier.
Consider its four orthogonal neighbors.
Only a valid fresh neighbor can be newly infected.
Mark it rotten immediately to prevent duplicate enqueues from other neighbors.
Reduce the number of remaining fresh oranges.
Queue this cell to spread infection in the next frontier.
After the entire frontier, one minute of simultaneous spreading has elapsed.
If fresh oranges remain return −1; otherwise return the elapsed minutes, possibly zero.
''')
notes('course-schedule', '''
Determine whether all n courses can be completed under the prerequisite edges.
Use a deque for the queue of courses ready to take.
Create an independent dependent-course list for every course.
Track how many unfinished prerequisites each course has.
Read each pair as a depends on b.
Record that finishing b can help unlock a.
Count that prerequisite against a.
Queue all courses requiring no prerequisites initially.
Count how many courses are actually removed from the dependency graph.
Continue while at least one course is ready.
Take a ready course from the front.
Count it as completed.
Visit every course that depends on this completed course.
Remove one unfinished prerequisite from that dependent.
Zero remaining prerequisites means this course is now ready.
Enqueue it exactly when it becomes ready.
All n processed means no cycle blocked any remaining component.
''')
notes('merge-k-sorted', '''
Accept sorted arrays and return their combined sorted values, preserving duplicates.
Import heapq, whose merge function lazily merges sorted streams.
Expand the arrays as separate inputs to heapq.merge, which keeps each stream's next candidate in a heap; materialize that ordered stream as a list.
''')
notes('subsets', '''
Return all subsets of distinct input values.
Start with the empty subset, which exists even for empty input.
Consider whether to include each next value.
Keep existing subsets without x and append new copies with x, covering both choices once.
Return the complete power set.
''')
notes('word-search', '''
Check whether a word can be traced through distinct orthogonally adjacent cells.
Save board dimensions for boundary checks; this contract uses a nonempty board.
Define a search at row i, column j, matching word position k.
If every character has already matched, the path succeeded.
Return success without requiring another cell.
Reject out-of-bounds positions and cells that do not contain the required next character.
Return failure for this path branch.
Save the original cell so it can be restored after exploration.
Mark this cell as unavailable to prevent reuse within the same path.
Try four possible neighbors for the next character, stopping once one branch succeeds.
Restore the cell so other candidate paths can use it independently.
Return this path's outcome after restoration.
Try every starting cell and return whether any search succeeds.
''')
notes('unique-paths', '''
Count right/down paths through an m-by-n grid.
The first row has one path to every cell, obtained by moving only right.
Process each subsequent row.
Skip the first column, whose path count remains one.
Add paths from above (old dp[j]) and left (already updated dp[j−1]).
The last entry now holds the count for the bottom-right cell.
''')
notes('climb-stairs', '''
Count ways to climb n positive steps using moves of one or two.
Seed the counts for zero and one step as one way each.
Advance the recurrence until reaching n steps.
Shift the previous count and add the preceding two counts; tuple assignment uses both old values.
Return the most recent count.
''')
notes('house-robber', '''
Return the best nonadjacent sum for the line of house values.
Track the best totals before the previous house and through the previous house.
Consider each new house value.
Either skip this house (b) or take it with the best nonadjacent total (a+x); update both saved totals simultaneously.
Return the best total through the last house, or zero for empty input.
''')
notes('word-break', '''
Decide whether s can be split into dictionary words.
Use a set for fast membership checks of candidate words.
Only the empty prefix is initially segmentable; later prefixes begin unresolved.
Build the answer for every prefix length from one through the full string.
Try split j: the earlier prefix must be valid and the remaining slice a word. any stops at the first successful split; Python slicing copies characters.
Return whether the entire string is segmentable.
''')
notes('coin-change', '''
Find the minimum coin count for a nonnegative amount, or −1 if impossible.
Zero amount needs zero coins; initialize positive amounts as unreachable infinity.
Solve smaller amounts before larger amounts that depend on them.
Try each available positive denomination as the final coin.
Only use a denomination that fits the current amount.
Compare the current best with one coin plus the best solution for the remainder.
Translate unreachable infinity into −1; otherwise return the minimum count.
''')
notes('lis', '''
Return the length of the longest strictly increasing subsequence.
Import binary search to locate a value's position among sorted tails.
Keep the smallest possible tail for each achievable subsequence length.
Consider input values in their original order; subsequences cannot reorder them.
Find the first tail ≥x so equal values do not extend a strictly increasing sequence.
A position beyond all existing tails means x extends the longest sequence.
Append x to represent that newly achievable length.
Otherwise replace an existing tail with a value no larger.
A smaller tail preserves the length while making future extension easier.
The number of tails equals the longest achievable length; tails itself need not be a subsequence.
''')
notes('jump-game', '''
Decide if the final index is reachable using each position's maximum jump length.
Initially only index zero is known to be reachable.
Inspect every position with its allowed jump.
If this position is past our best reach, no earlier reachable position can get here.
Stop with failure; later values cannot bridge an already unreachable gap.
Extend reach using this reachable position's jump if it improves the boundary.
Every position was reachable, so the final position is reachable too.
''')
notes('set-zeroes', '''
Return a same-shaped matrix with every original zero's row and column zeroed.
Collect the indices of rows containing an original zero.
Collect column indices of original zeros across all rows.
Build new rows, replacing a value only if its row or column was recorded; new zeros cannot contaminate discovery.
''')
notes('softmax', '''
Convert a nonempty finite score vector into probabilities summing to one.
Import exponential arithmetic.
Find the largest score for a numerically safe shift.
Exponentiate each shifted score; all exponents are nonpositive, preventing overflow.
Sum the unnormalized positive weights.
Divide each weight by the same total; the shared shift cancels mathematically.
''')
notes('cosine-sim', '''
Compare the directions of two equal-length vectors.
Import square root for Euclidean norms.
Compute the first vector's length from the sum of squared coordinates.
Compute the second vector's length the same way.
Check for a zero vector before division.
Return the exercise's explicit zero-vector convention, since mathematical cosine is undefined there.
Multiply matching coordinates, add them, and divide by both lengths to remove positive scale differences.
''')
notes('kv-cache', '''
Estimate bytes for one sequence's keys and values using explicit model dimensions and storage precision.
Multiply keys-and-values factor 2, layers, KV heads, head dimension, cached tokens, and bytes per element. This excludes allocator overhead and batching.
''')
notes('tokens-per-sec', '''
Estimate the ideal batch-one weight-bandwidth ceiling from model size and bandwidth.
Convert billions of parameters times bits per weight into decimal gigabytes by dividing by eight.
Divide GB per second by model GB and round for display; this is an estimate, not a device benchmark.
''')
notes('rrf', '''
Fuse ranked document lists using inverse rank with smoothing k.
Accumulate combined scores by document ID.
Process each retriever's ordered list.
Use ranks starting at one, as required by the RRF formula.
Add this retriever's vote, treating a document not yet seen as having zero accumulated score.
Sort by negative score for descending relevance and by ID for deterministic ties, then return only IDs.
''')
notes('rslora', '''
Calculate the adapter update scale for LoRA or rsLoRA at a positive rank.
Import square root for the rank-stabilized denominator.
Use sqrt(r) for rsLoRA and r otherwise, divide alpha by that denominator, then round to two decimals.
''')
notes('lru-cache', '''
Define an object that preserves cache contents and recency across calls.
Initialize a cache instance with a maximum entry count.
Import OrderedDict for efficient keyed lookup plus editable key order.
Start with no stored entries; oldest access stays at the front.
Save the capacity on the object for later eviction checks.
Define lookup by key.
Check absence before indexing the dictionary.
Return the missing-key sentinel −1 without changing recency.
A successful read makes this key most recently used, so move it to the end.
Return the stored value after updating its recency.
Define insertion or replacement for a key.
Store the new value; replacing an existing key does not add another entry.
A write also counts as recent use, so move the key to the end.
Eviction is needed only when the entry count exceeds capacity.
Remove the first, least-recently-used entry with last=False; put implicitly returns None.
''')
notes('trie', '''
Define a prefix tree that shares character paths between inserted words.
Create an empty trie instance.
The root is a dictionary of first-character branches.
Define insertion of one word.
Begin traversal at the root.
Walk through the word's characters in order.
Reuse the matching branch or create an empty child dictionary, then move into it.
Mark this path as a complete word with the reserved $ terminator.
Define exact-word lookup, which differs from prefix lookup.
Start at the root again for each independent search.
Follow the requested word one character at a time.
A missing branch means this word was never inserted.
Stop immediately with failure.
Move into the matching child dictionary.
Accept only if the path ends at a word marker, not merely an existing prefix.
Define a query asking whether any stored word begins with this prefix.
Begin at the root.
Read each prefix character.
A missing branch makes the prefix impossible.
Return False at the first missing branch.
Follow an existing branch.
Reaching the end of the prefix is sufficient; a word marker is not required.
''')
notes('meeting-rooms', '''
Find the peak number of simultaneous half-open meetings.
Import heap operations to efficiently find the earliest finishing active meeting.
Store active meeting end times in a min-heap.
Start the peak overlap count at zero.
Process meetings by start time so finished meetings can be discarded permanently.
Release all rooms whose meetings end at or before this start.
Remove the earliest finished meeting from the heap.
Add the current meeting's end because it occupies a room now.
Record the largest active meeting count seen so far.
Return that peak, not the number active at the final start time.
''')
notes('min-tree-depth', '''
Find the nearest leaf in a level-order encoded tree.
Use a deque to process the tree breadth-first.
Convert the input list into nodes with the shared helper; that helper is outside this solution's line trace.
An empty tree contains no root-to-leaf path.
Return zero for empty input.
Queue the root at depth one, counting nodes rather than edges.
Continue while nodes remain to visit.
Take the earliest queued node and its depth.
A leaf has neither a left nor a right child.
BFS guarantees this first leaf has the smallest depth, so return immediately.
Consider both children in left-to-right order.
Only real child nodes should be queued.
Each child is one level deeper than its parent.
''')
notes('vertical-order', '''
Group tree values into columns while retaining breadth-first order within a column.
Import default lists for columns and a FIFO queue.
Build nodes from the level-order input using the shared tree helper.
Handle the tree with no nodes.
Return no columns for that empty tree.
Create an output list automatically when a column is first encountered.
The root starts at horizontal column zero.
Process pending nodes breadth-first.
Take a node together with its assigned column.
Append its value; BFS preserves row order and left-to-right ties.
Check whether a left child exists.
Queue it one column to the left.
Check whether a right child exists.
Queue it one column to the right.
Return column lists ordered by their column indices, not by their stored values.
''')
notes('restore-ip', '''
Generate valid dotted IPv4 addresses by partitioning the digit string.
Collect complete valid addresses here.
Define a search from character position pos with the parts chosen so far.
Calculate how many of the four parts remain to be formed.
Prune when the remaining characters cannot fit 1–3 digits per remaining part.
Stop exploring this impossible split.
Zero remaining parts means all four are complete; the earlier length check ensures no characters remain.
Join the chosen parts with dots to create one valid address.
Finish this complete branch without adding another part.
Try part lengths of one, two, and three digits.
Take a candidate substring starting at the current position.
Reject a requested length extending beyond the string.
Longer lengths also cannot fit, so exit the length loop.
A multi-digit part beginning with zero is forbidden.
Longer parts would share that leading zero, so stop trying them too.
Accept the candidate only when its numeric value is within IPv4's upper bound.
Continue after this part, passing a new parts list so sibling branches remain independent.
Start with no digits consumed and no parts chosen.
Sort the completed addresses to meet the deterministic output contract.
''')
notes('nested-weight', '''
Compute the depth-weighted sum of integers nested inside lists.
Define recursion with an explicit current depth.
Multiply an integer by its depth; otherwise recurse into the nested list at depth+1, and add all contributions.
Top-level integers start at weight one.
''')
notes('merge-unique', '''
Combine sorted arrays into an increasing list without repeated values.
Use heapq.merge to emit all inputs in sorted order without sorting them again.
Start with an empty deduplicated result.
Read values from the merged stream; duplicates arrive next to one another.
Keep a value only when the result is empty or it differs from the last kept value.
Append this newly encountered distinct value.
Return the unique sorted output.
''')
notes('logger-cooldown', '''
Decide whether each timestamped message may be accepted under a per-message cooldown.
Remember only the last accepted timestamp for each message.
Collect one acceptance decision per event.
Process events in the guaranteed nondecreasing timestamp order.
Accept a new message or one whose elapsed time reaches the cooldown boundary.
Record the decision even for rejected events.
Only an accepted event should update the cooldown state.
Save its timestamp so rejections do not postpone the next permitted message.
Return decisions in original event order.
''')
notes('recipe-dependencies', '''
Resolve all recipes whose ingredients become available from supplies and other recipes.
Use reverse-dependency lists and a queue of available recipes.
Map each missing ingredient to recipes waiting for it.
Track each recipe's number of unavailable distinct ingredients.
Use a set for fast supply membership and duplicate elimination.
Pair each recipe with its ingredient list.
Remove already supplied ingredients and count each requirement only once.
Save the recipe's missing-requirement count.
Visit every unavailable ingredient needed by this recipe.
Record the waiting recipe under that ingredient for later release.
Initially queue recipes with no missing requirements or recipes already supplied.
Track recipes already emitted so each available name releases dependents once.
Continue while an available recipe can unlock other recipes.
Take one available recipe from the queue.
Ignore repeat queue entries for a recipe already processed.
Skip duplicate processing, avoiding repeated indegree decrements.
Record that this recipe is now available and processed.
Visit recipes that were waiting for this ingredient.
Satisfy this one missing dependency.
A recipe with zero remaining requirements is now buildable.
Queue it to release its own dependents.
Return buildable recipe names sorted for deterministic output; unavailable cycles are omitted.
''')
notes('sparse-matvec', '''
Multiply a sparse coordinate-list matrix by a dense vector.
Allocate zero for each output row; omitted matrix cells contribute nothing.
Visit only stored matrix entries, including any repeated coordinates.
Add this entry's value times the matching vector coordinate into its output row.
Return the accumulated dense output vector.
''')
notes('lazy-map', '''
Find the first input index reaching target after the ordered transformation chain.
Evaluate one input value at a time, allowing early exit.
Read each affine transformation in its specified order.
Apply multiplication and offset to the current working value.
Check the fully transformed value only after the complete chain.
Return immediately on the first match, avoiding later inputs' work.
If no element matched, return the absence sentinel.
''')
notes('hit-counter', '''
Answer recent-hit counts over the half-open window (now−window,now].
Use a FIFO deque because timestamp order is guaranteed.
Keep active hit timestamps, preserving duplicates as separate hits.
Collect a result for every operation.
Process hit/count events in timestamp order.
Expire hits at or before the excluded left boundary.
Remove the oldest expired timestamp; repeat until the front is still active.
A hit adds one new event to the current window.
Append its timestamp; equal-time hits each occupy an entry.
A hit operation returns None under this exercise's contract.
The other permitted operation requests the current count.
Return the number of timestamps still inside the active window.
Return all operation results in order.
''')
notes('bounded-crawler', '''
Find page IDs within a maximum number of edges from a starting page.
Use a queue so first discovery is always by a shortest path.
Mark the start as discovered even if it has no outgoing links.
Queue the start at distance zero.
Continue through the current frontier until it is empty.
Take the next page and its shortest discovered depth.
At the depth limit, the page is included but its neighbors must not be expanded.
Skip expansion for that page.
Read outgoing links; a missing page entry is treated as having none.
Only undiscovered neighbors need to be queued.
Mark before enqueuing to prevent duplicate links and cycles from adding repeated work.
Queue the neighbor one edge farther away.
Return reachable IDs in sorted order rather than traversal order.
''')
notes('resumable-iterator', '''
Simulate reading, saving, and restoring a cursor into fixed values.
Cursor zero means the first item is the next unread one.
Store one result for every requested operation.
Process operations sequentially because each changes the meaning of the next.
Handle a request to read the next value.
The cursor equal to the length is the stable exhausted state.
Return None without advancing beyond exhaustion.
Otherwise an unread item exists.
Return the item at the next-unread position.
Advance exactly once after returning that item.
Handle a save request independently of reading.
Return the current next-unread index as a resumable state.
The remaining valid operation is restore.
Replace the cursor with the caller's valid saved position.
Restore has no returned data under this contract.
Return the operation results, including saved positions.
''')
notes('mini-database', '''
Filter flat rows by equality and return matching IDs in stable sort order.
Keep a row only when every requested field exists and equals its filter; missing is different from an explicit None.
Stable-sort matching rows by the requested field and extract IDs, retaining original order for equal sort values.
''')
notes('ttl-lru', '''
Simulate a cache whose entries have both recency order and independent expiration times.
Import an ordered dictionary for efficient recency updates.
Start with no entries; values store (payload,expiry).
Collect one return value per operation.
Process operations in nondecreasing time order.
Read the operation name, timestamp, and key from its shared prefix.
Iterate a copy of keys so expired entries can be deleted safely during this scan.
An expiry at or before now is no longer valid.
Remove it before capacity eviction so a dead entry cannot displace a live one.
Handle insertion or update.
Store the new payload and reset expiry to now+ttl.
A put makes this entry most recently used.
Check whether the live entry count exceeds capacity, including capacity zero.
Evict the oldest live key by removing the front entry.
Record None because put is a mutation, not a lookup.
For a get, check whether the requested key survived expiration cleanup.
Refresh recency on a successful get without changing its expiry.
Return the stored payload, omitting the expiry metadata.
Otherwise the key is missing or expired.
Return −1 for that cache miss.
Return all operation results; note that the expiration scan makes this teaching version O(capacity) per operation.
''')
notes('word-abbreviation', '''
Check whether literal letters and numeric skips consume exactly the whole word.
Start separate cursors for the word and abbreviation.
Continue until the abbreviation is fully read.
A digit begins a whole skip count, possibly several digits long.
Zero cannot begin a valid skip, rejecting both zero and leading zeros.
Return False for that invalid count.
Start accumulating this digit run's numeric value.
Read every consecutive digit before applying the skip.
Multiply the previous count by ten and add the next digit.
Advance the abbreviation cursor past each digit consumed.
Move the word cursor forward by the complete skip count.
Reject a skip that runs past the end of the word.
Return False for that overshoot.
Otherwise the abbreviation character must match a literal word character.
Reject if the word is already exhausted or the letters differ.
Return False because this literal cannot match.
Advance past the matched word character.
Advance past the matched abbreviation character.
Accept only if the word cursor also reached the exact end.
''')
notes('fast-power', '''
Compute a finite power with an integer exponent by repeated squaring.
A negative exponent means taking a reciprocal power.
Invert the base and make the exponent positive before processing its bits.
Initialize the product identity, also producing one when n=0.
Process the exponent until all binary digits have been consumed.
A set least-significant bit means the current base power belongs in the answer.
Multiply it into the accumulated result.
Square the base to represent the next binary power.
Discard the processed bit using integer division by two.
Return the accumulated power.
''')
notes('min-stack', '''
Simulate a stack supporting constant-time retrieval of the current minimum.
Each stored pair holds (value,minimum through this position).
Collect returned values for each operation.
Process operations in their given order.
Handle pushing a new item.
Read the pushed value.
Store it with the smaller of itself and the previous prefix minimum; an empty stack uses itself.
Push returns no value.
A pop removes the last pair and returns only its value, automatically restoring the earlier minimum.
A top request reads the current value without removing it.
A min request reads the saved prefix minimum without scanning the stack.
Return all operation results.
''')
notes('generate-parentheses', '''
Generate all balanced strings containing n pairs of parentheses.
Collect complete valid strings here.
Track the current text and how many open/close brackets it contains.
When n closing brackets are placed, all pairs are complete.
Save that complete string.
Stop this branch so it cannot add extra characters.
Add an opener only while fewer than n have been used.
Recurse with the new opening bracket; trying it first preserves lexical order.
A closer is legal only when an unmatched opener exists.
Recurse with one more closer, preserving valid nesting at every prefix.
Start with empty text and zero used brackets of each type.
Return all generated strings, including the empty string when n=0.
''')
notes('find-duplicate', '''
Find the repeated value by treating the constrained array as a pointer graph.
Start both pointers at the same first reachable value.
Move at least once before comparing so initial equality is not mistaken for a cycle meeting.
Follow one pointer edge for the slow pointer.
Follow two edges for the fast pointer.
Their next meeting proves they are inside the cycle.
Exit the first phase at that meeting.
Reset one pointer to the graph's starting value.
Move both at equal speed until they meet at the cycle entrance.
Advance the reset pointer one edge.
Advance the meeting pointer one edge as well.
The shared entrance value is the duplicate under the 1..n input constraints.
''')
notes('sparse-dot', '''
Compute a dot product using coordinate dictionaries rather than dense vectors.
Check which input has more nonzero entries.
Swap references so a is the smaller map and fewer coordinates need inspection.
For each coordinate in a, multiply by b's matching value or zero if absent, then sum the contributions.
''')
notes('nearest-neighbors', '''
Return indices of the k nearest vectors by squared Euclidean distance.
Store a distance/index pair for each candidate.
Process each vector together with its original index.
Sum squared coordinate differences; square roots are unnecessary because they preserve ordering.
Pair the distance with the index so ties favor smaller indices automatically.
Sort pairs, keep the first k, and return only their indices.
''')
notes('kmeans-step', '''
Perform one assignment-and-mean-update iteration using the supplied old centers.
Count the number of points assigned to each cluster.
Allocate independent coordinate sums for each center.
Assign each point using the unchanged old centers.
Find the index minimizing squared distance; min keeps the earliest index on a tie.
Count this point in its chosen cluster.
Read the point's coordinate index and value.
Accumulate that coordinate into the chosen cluster's sum.
Divide each cluster's sums by its count; preserve an old center when no points joined it.
''')
notes('linear-gradient', '''
Take one full-batch step minimizing mean squared error, without a bias term.
Allocate a zero gradient accumulator per weight.
Pair each feature row with its target.
Compute the current prediction as a dot product and subtract the target to obtain signed error.
Calculate each feature's contribution to the weight gradient.
Add 2×error×feature/n, the derivative of mean squared error for this row.
Update each weight only after the whole batch gradient is accumulated.
''')
notes('stable-sigmoid', '''
Compute sigmoid probabilities while avoiding exponential overflow.
Import the exponential function.
Collect probabilities in input order.
Process one logit at a time.
For nonnegative x, −x is safe to exponentiate.
Use the standard sigmoid expression with a nonpositive exponential argument.
For negative x, use an algebraically equivalent expression.
Exponentiate x itself, which is negative and cannot overflow upward.
Divide e by 1+e; very negative x safely approaches probability zero.
Return the probabilities.
''')
notes('binary-log-loss', '''
Compute average binary cross-entropy directly from logits and matching labels.
Use log1p for accurate log(1+small_value) and exp for the stable tail term.
For each pair use max(z,0)−z*y+log1p(exp(−abs(z))), then average; the exponential never receives a positive argument.
''')
notes('classification-metrics', '''
Compute positive-class precision, recall, and F1 with an explicit zero-denominator convention.
Count pairs where both the actual and predicted label are positive.
Count predicted positives whose actual label is negative.
Count actual positives that the classifier missed.
Divide correct positive predictions by all positive predictions, or return zero if none exist.
Divide found positives by all actual positives, or return zero when there are none.
Use the count-based harmonic-mean formula, guarding its denominator too.
Return metrics in the declared precision, recall, F1 order.
''')
notes('confusion-matrix', '''
Count each true/predicted label combination for a multiclass classifier.
Create independent zero-filled rows; repeating one shared row would corrupt all counts.
Visit paired ground-truth and predicted labels.
Increment the cell whose row is actual and whose column is predicted.
Return the count matrix, retaining empty classes as zero rows or columns.
''')
notes('recall-at-k', '''
Measure the fraction of relevant documents found within the first k ranking positions.
Deduplicate ground-truth IDs so a document contributes once to the denominator.
Intersect unique top-k IDs with relevant IDs, divide by relevant count, and use zero when the ground-truth set is empty.
''')
notes('ndcg', '''
Score a ranked candidate set against its own ideal ordering at cutoff k.
Import logarithm base two for position discounts.
Define discounted cumulative gain for one candidate ordering.
Give each top-k grade gain 2^grade−1 and discount by log2(index+2), converting zero-based positions to the rank formula.
Sort grades descending to calculate the maximum achievable gain for these candidates.
Normalize actual gain by ideal gain; return zero when all available gain is zero.
''')
notes('overlap-chunks', '''
Split tokens into bounded chunks with an explicit overlap and no redundant final chunk.
Collect emitted token slices.
Start the first chunk at the beginning of the token list.
Continue only while some token is still available at the current start.
Copy at most size tokens into this chunk.
If this chunk reaches the end, the input has been fully covered.
Stop instead of emitting another chunk contained within this final chunk.
Advance by size−overlap so adjacent chunks share exactly the requested overlap when both are full.
Return the chunks, or an empty list for empty input.
''')
notes('tfidf', '''
Build sparse TF–IDF feature dictionaries from already-tokenized documents.
Use natural logarithms for the chosen smoothed IDF formula.
Import Counter to collect word occurrence frequencies.
Count each token once per document using set(document), producing document frequency rather than total frequency.
Collect one score dictionary per document.
Process documents independently using the shared corpus frequencies.
Count repeated occurrences within the current document for term frequency.
For each present token multiply count/document_length by log((1+document_count)/(1+document_frequency))+1; empty documents produce an empty dictionary without division.
Return all document feature dictionaries.
''')
notes('attention', '''
Compute one query's scaled dot-product attention over key/value pairs.
Import square root and exponential for scaling and normalization.
Compute each query–key dot product and divide by sqrt(query_dimension).
Find the largest score so exponentials can be shifted safely.
Exponentiate shifted scores; these are nonnegative unnormalized mixing weights.
Sum those weights to obtain their common normalization denominator.
For each value coordinate, sum its weighted contributions and divide by the denominator to produce the output vector.
''')
notes('layer-norm', '''
Normalize a nonempty feature vector using population variance and positive epsilon.
Import square root for the standard-deviation denominator.
Compute the average feature value.
Average squared deviations from the mean; use n, not the sample-variance denominator n−1.
Add epsilon before the square root to keep constant vectors well-defined.
Center each feature and divide by the same scale; learned gamma and beta are omitted here.
''')
notes('token-batches', '''
Group contiguous requests under a token-sum budget while preserving arrival order.
Collect completed batches of request indices.
Start an empty current batch.
Track its current token total.
Read each request length with its index.
If adding this request exceeds budget, the current batch must close first.
Save the finished batch before creating the next one.
Reset both batch contents and budget usage together.
Add the request's index to the active batch.
Account for its tokens in the batch total.
The final partial batch still needs to be saved when nonempty.
Append that last batch exactly once.
Return batches of indices, not token lengths.
''')
notes('request-dedup', '''
Identify equivalent JSON requests without confusing textual formatting with object equality.
Import the JSON parser rather than manipulating raw strings.
Map each canonical object representation to its first input index.
Collect the first-equivalent index for every request.
Process requests in order so the earliest occurrence wins.
Parse the request; whitespace outside values no longer affects equality.
Sort object key/value pairs and turn them into a hashable tuple under the flat string-value contract.
Only a genuinely new canonical request should create an entry.
Save its first index and never overwrite that index on retries.
Return the stored first occurrence for this request.
Return the index list, preserving the original request order.
''')
notes('subscription-events', '''
Build a deterministic notification schedule from subscriptions and reminder offsets.
Collect dated events before sorting them.
Read each subscription's user, start day, and end day.
Always add welcome and expiration events at their specified dates.
Deduplicate offsets so repeated offsets cannot emit duplicate reminders.
Only reminders on or after the start belong to this subscription.
Add the reminder at end−offset with its user and event type.
Sort by day, then user, then event name as declared in the exercise; this schedules data and sends no messages.
''')
notes('token-bucket', '''
Decide which requests fit a continuously refilling token bucket.
Start at full capacity, using a float because fractional tokens can refill between requests.
Set the initial time origin to zero.
Collect acceptance decisions.
Read nondecreasing request timestamps.
Refill by elapsed time×rate but never store more than capacity.
A request needs at least one full token.
Only accepted requests consume capacity.
Subtract exactly one token for this request.
Record the decision in request order.
Update the timestamp even after rejection so the same elapsed time is not counted twice.
Return all decisions.
''')
notes('dense-rank', '''
Return descending dense ranks within each group while preserving row order.
Import default sets for each group's distinct scores.
Create each group's set on first use.
Read group and score from every row.
Store each distinct score once because ties share a dense rank.
Sort each group's scores descending and map them to consecutive one-based ranks.
Look up those ranks in the original row order instead of returning the sorted rows.
''')
notes('bounded-async', '''
Define an awaitable solution; the runner awaits it rather than using asyncio.run inside an active event loop.
Import asyncio for cooperative tasks and awaitable work.
Allocate result slots by input index so output order does not depend on completion order.
Share one iterator of (index,value) jobs between a bounded number of workers.
Define one worker coroutine that repeatedly obtains a job and processes it.
Take the next job with no intervening await, so event-loop workers cannot claim the same iterator entry.
Yield to simulate an I/O wait; this does not make CPU computation parallel.
Store the result in its original index, regardless of which worker finishes first.
Start no more than limit workers (or the number of items) and await all of them; starred expansion passes each coroutine to gather.
Return the ordered results only after every worker completes.
''')
# Explicit branch lines are separate after formatting the original compact source.
LESSONS['min-stack'][8:] = [
 'Recognize a request to remove the latest pushed value.',
 'Remove the final pair and return its value; the previous prefix minimum is restored automatically.',
 'Recognize a request to inspect the top without removing it.',
 'Return the value component of the final pair.',
 'The remaining allowed request is the current minimum.',
 'Return the saved prefix minimum without scanning the stack.',
 'Return all operation results in input order.'
]
notes('confidence-abstention', '''
Choose a class only when the confidence and separation policy is satisfied.
Check for the absence of any candidate scores.
Return the abstention sentinel when there is nothing to rank.
Sort class indices by descending score and then ascending index to define tie behavior.
The first ranked index is the candidate winner, not yet authorized to act.
Read the runner-up score, using zero for the single-class contract.
Require both a sufficiently high score and a sufficiently large lead over the runner-up.
Return the winning class index only after both conditions pass.
Otherwise abstain; downstream code can ask for clarification instead of guessing.
''')
notes('field-validation', '''
Validate required field shapes for a list of extracted records.
Collect one invalid-field list per record.
Inspect records independently so each has its own validation result.
Start this record with no identified invalid fields.
Check every field required by the submission contract.
Look up the value; a missing field becomes None and will fail the string check.
Reject a non-string or a string that becomes empty after trimming; short-circuiting avoids calling strip on non-strings.
Record the invalid field name, continuing to discover all errors.
Sort error names to make reports deterministic and easy to compare in tests.
Return the per-record error lists without modifying source records.
''')
notes('action-receipts', '''
Simulate authorization, cancellation, and receipt-based duplicate protection.
Map executed operation IDs to their exact payloads.
Collect a status for every request.
Read each request's identity, payload, authorization, and cancellation state.
Enforce authorization before any receipt or execution decision.
A denied request produces a status but no stored execution receipt.
Next check whether this eligible request has been cancelled.
Record cancellation without executing or reserving the ID.
An existing receipt means this ID has already executed.
The same payload replays the old result; a different payload conflicts with the ID's existing meaning.
Otherwise this is an eligible operation with a new ID.
Store the payload binding as the simulated execution receipt.
Report execution once for this ID; no actual external operation occurs here.
Return statuses in request order.
''')
notes('pagerank-step', '''
Compute one synchronous PageRank update from a fixed vector of old ranks.
Count nodes so teleport and dangling mass can be shared uniformly.
Add old ranks of nodes with no outgoing destinations; their probability mass must not disappear.
Initialize every new rank with its teleport contribution plus its share of dangling mass.
Visit each node and its outgoing destinations.
Only non-dangling nodes have edges across which to distribute rank.
Split the node's damped old rank equally among its outgoing edges.
Visit each receiving node.
Add this edge's contribution to the receiver's new rank.
Return the completed next iteration; the input ranks remain unchanged.
''')
