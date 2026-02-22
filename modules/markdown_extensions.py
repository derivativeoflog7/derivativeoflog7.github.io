"""
Baesd on:
    https://github.com/Python-Markdown/markdown
"""
"""
BSD 3-Clause License

Copyright 2007, 2008 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

    Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import re
import xml.etree.ElementTree as etree
from markdown import inlinepatterns

class ExtendendLinkInlineProcessor(inlinepatterns.LinkInlineProcessor):
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        """ Return an `a` [`Element`][xml.etree.ElementTree.Element] or `(None, None, None)`. """
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("a")
        el.text = text

        el.set("href", href)

        if title is not None and title != '':
            # Hijack title, which now also includes attributes
            split_title = title.split("|")
            # Actual title is the first element
            attributes = split_title[1:]
            parsed_attributes = 0
            if len(attributes) == 0:
                return None, None, None
            title = split_title[0]
            if title != '':
                el.set("title", title)
            if "newpage" in attributes:
                parsed_attributes += 1
                el.set("target", "_blank")
                el.set("rel", "noopener noreferrer")

            # If there are more attributes than were able to parse, abort and let the builtin parser handle it
            if parsed_attributes != len(attributes):
                return None, None, None

        else:
            # Let the builtin parser handle it
            return None, None, None

        return el, m.start(0), index
