# caches_WC package

This Python package provides basic least-recently-used (LRU) cache and
least-frequently-used (LFU) cache implementations for data in the form of simple key-value pairs.

## Background

A cache is typically used as a small section of memory to hold data or
references to data for fast and easy access. Data is often looked up using `key`s,
which are the classifiers used for their corresponding values. Since a cache
must be limited in size to support fast and efficient look ups, a client will
typically only want to store "valuable" entries in the cache. A client's idea
of "valuable" may vary but generally it is useful to only store the pieces of
data which are "relevant" at any given time.

Often, a `capacity` for the cache is provided, acting as an upper limit on the
number of elements that can be in the cache. While the number of entries in the
cache is less than the `capacity`, new `key`-`value` pairs can be placed in the
cache. Updating the `value` for a `key` already in the cache or
looking up the `value` associated with a `key` will be possible no matter how many
entries are in the cache.

When the cache is at its full capacity and the client wishes to enter a data
pair such that the pair's `key` is not in the cache, an entry of the cache must
be evicted to make room for the new `key`-`value` pair. There are various strategies
for determining the entry to be evicted and the best approach can depend on the
application, but two well-known ones are the least-recently-used (LRU) and
least-frequently-used (LFU) protocols.

As the name suggests, the entry evicted using the LRU protocol is the one whose
`key` has been operated on the least recently, that is, the one that has
experienced a `key`-`value` setting, a value update, or a look up operation the
least recently.

Similarly, the entry evicted using the LFU protocol is the one whose `key` has
been operated on the least frequently of all entries in the cache, where an
operation is also any of the three of setting a `key`-`value` pair, updating the
`value` associated with a `key` in the cache, or looking up the `value` associated
with a `key`. When there is more than one pair that has been operated on the
least frequently, the one least recently used is evicted. When an entry is
evicted, its frequency is marked as `0` for later entries of that `key` into the
cache.

In practice, LRU caches are more common than LFU caches as new entries looked up
can commonly be evicted immediately in an LFU cache; for example, consider an instance when all entries
except that for a `key` A have frequency at least 2 and A has frequency 1. Then
adding a new `key` B evicts A, then adding A again evicts B, then adding B evicts
A, etc, yielding no speed up in look-up times for A and B.

## Design

This package was designed with Python object-oriented programming best practices in mind.
The LRU cache and LFU cache classes each inherit from a common `Cache` class.
The entries themselves are represented as nodes with keys, values, and
additional data, with `LRUNode` and `LFUNode` classes inheriting from a common
`CacheNode` class.

To ensure O(1) time operations for look ups and setting/editing key-value pairs
in the LRU cache, the cache is represented as a doubly linked list of entries along
with a hash map from keys to their corresponding nodes in the linked list. Using
 the hash map, look ups and setting/editing can be done in O(1) time.
Furthermore, evicting entries is as easy as removing the last node in the doubly
 linked list, while marking a key as having just been operated on is done by
placing the corresponding node at the beginning of the linked list, removing it
from its current location in the linked list if necessary. All of this can be
done in O(1) time (assuming constant time look ups in the hash map, which is
represented as a dictionary in Python), including operations to maintain the
structure of order of recent usage and to facilitate evictions.

Similarly, to ensure O(1) time operations for look ups and setting/editing
key-value pairs in the LFU cache, a hash map from keys to their corresponding
nodes exists. To maintain frequency counts, a top-level linked list is used
whose nodes represent the different frequencies of keys in the cache. These
frequency nodes each have an associated LRU cache containing all nodes
corresponding to key-value pairs with the frequency node's listed frequency.
Look ups and setting/editing are O(1) operations assuming constant time look ups
 for the hash map (also represented as a dictionary), including the operations
to maintain the frequency structure and to facilitate evictions.

## API

The basic client API includes the following methods:

### LRU Cache
- `LRUCache(capacity : int)`: a constructor for an LRU cache which takes an
optional `int` parameter for the capacity of the cache. If no capacity parameter
is provided, the capacity of the LRU cache is set to `10`. An error will be
thrown if the provided parameter for capacity is not a positive integer.
- `get_value(key)`: an O(1) time look-up function to return the value
associated with `key` in the cache. If `key` is not present in the cache, return
 `None`. If the key does exist in the cache, it is updated as the most recently
used entry. `key` must be hashable.
- `put_key_value(key, value)`: an O(1) time setting/editing operation.
If `key` exists in the cache, its corresponding value is set to `value`. If
`key` does not exist in the cache, it is added to the cache with the value
`value`, evicting the least recently used entry if the cache is at capacity. Again, `key` must be hashable.

### LFU Cache
- `LFUCache(capacity : int)`: a constructor for an LFU cache which takes an
optional `int` parameter for the capacity of the cache. If no capacity parameter
is provided, the capacity of the LRU cache is set to `10`. An error will be raised if the provided parameter for capacity is not a positive integer.
- `get_value(key)`: an O(1) time look-up function to return the value
associated with `key` in the cache. If `key` is not present in the cache, return
 `None`. If the key does exist in the cache, its frequency tally is updated. `key` must be hashable.
- `put_key_value(key, value)`: an O(1) time setting/editing operation.
If `key` exists in the cache, its corresponding value is set to `value`. If
`key` does not exist in the cache, it is added to the cache with the value
`value`, evicting the least frequently used entry if the cache is at capacity (and the least recently used among all least frequently used if more than one is
least frequently used). The frequency tally of the entry corresponding to `key`
is updated accordingly. Again, `key` must be hashable.

## Downloading

If you have the Python package manager `pip`, the package can be installed at the terminal with the following command:

```pip install caches_WC```

Alternatively, to download the original module files
 you can clone the `master` branch of this repository.
