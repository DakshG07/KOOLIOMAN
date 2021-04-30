"""
MIT License

Copyright (c) 2020-present shay (shayypy)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------------

This project includes code from https://github.com/Rapptz/discord.py, which is
available under the MIT license:

The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from .asset import Asset
from .file import File, MediaType
from .utils import ISO8601


class Group:
    def __init__(self, *, state, team, data):
        self._state = state
        self.team = team
        data = data.get('group', data)

        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.position = data.get('priority')

        self.game_id = data.get('gameId', 0)
        self.base = data.get('isBase')
        self.public = data.get('isPublic')
        
        self.created_by = self.team.get_member(data.get('createdBy')) or data.get('createdBy')
        self.updated_by = self.team.get_member(data.get('updatedBy')) or data.get('updatedBy')
        self.archived_by = self.team.get_member(data.get('archivedBy')) or data.get('archivedBy')

        self.created_at = ISO8601(data.get('createdAt'))
        self.updated_at = ISO8601(data.get('updatedAt'))
        self.deleted_at = ISO8601(data.get('deletedAt'))
        self.archived_at = ISO8601(data.get('archivedAt'))

        icon_url = data.get('avatar')
        if icon_url:
            self.icon_url = Asset('avatar', state=self._state, data=data)
        else:
            self.icon_url = None

        banner_url = data.get('banner')
        if banner_url:
            self.banner_url = Asset('banner', state=self._state, data=data)
        else:
            self.banner_url = None

    async def delete(self):
        return await self._state.delete_team_group(self.team.id, self.id)

    async def edit(self, **fields):
        if type(fields.get('icon')) == str:
            fields['icon_url'] = fields.get('icon')
        elif type(fields.get('icon')) == File:
            file = fields.get('icon')
            file.type = MediaType.group_icon
            fields['icon_url'] = await file._upload(self._state)
        elif type(fields.get('icon')) == type(None):
            fields['icon_url'] = None

        return await self._state.update_team_group(self.team.id, self.id, **fields)
