# Copyright (c) 2014 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class _Iterator(object):
    """Base Iterator

    This iterator is not meant to be used outside
    the scope of this package. The iterator gets
    a dictionary as returned by a listing endpoint.

    Subclasses of this base class determine the key
    to iterate over, as well as the means of creating
    the objects contained within.

    If there are no objects left to return, the iterator
    will try to load more by following the `next` rel link
    type.

    The iterator raises a StopIteration exception if the server
    doesn't return more objects after a `next-page` call.

    :param client: The client instance used by the queue
    :type client: `v2.Client`
    :param listing_response: Response returned by the listing call
    :type listing_response: Dict
    """
    def __init__(self, client, listing_response, iter_key, create_function):
        self._client = client
        self._iter_key = iter_key
        self._create_function = create_function

        self._links = []
        self._stream = False
        self._listing_response = listing_response

        # NOTE(flaper87): Simple hack to
        # re-use the iterator for get_many_messages
        # and message listing.
        if isinstance(listing_response, dict):
            self._links = listing_response.get('links', [])
            self._listing_response = listing_response[self._iter_key]

    def __iter__(self):
        return self

    def get_iterables(self, iterables):
        self._links = iterables['links']
        self._listing_response = iterables[self._iter_key]

    def stream(self, enabled=True):
        """Make this `_Iterator` a stream iterator.

        Since `_Iterator`'s default is to *not* stream,
        this method's default value is to *stream* data
        from the server. That is, unless explicitly specified
        this method will enable make this iterator a stream
        iterator.

        :param enabled: Whether streaming should be
                        enabled or not.
        :type enabled: bool
        """
        self._stream = enabled
        return self

    def _next_page(self):
        for link in self._links:
            if link['rel'] == 'next':
                # NOTE(flaper87): We already have the
                # ref for the next set of messages, lets
                # just follow it.
                iterables = self._client.follow(link['href'])

                # NOTE(flaper87): Since we're using
                # `.follow`, the empty result will
                # be None. Consider making the API
                # return an empty dict for consistency.
                if iterables:
                    self.get_iterables(iterables)
                    return
        raise StopIteration

    def __next__(self):
        try:
            args = self._listing_response.pop(0)
        except IndexError:
            if not self._stream:
                raise StopIteration

            self._next_page()
            return self.next()

        return self._create_function(args)

    # NOTE(flaper87): Py2K support
    next = __next__
