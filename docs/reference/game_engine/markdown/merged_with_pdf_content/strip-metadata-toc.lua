--[[
Pandoc Lua filter for FF7 game engine documentation merge
Created: 2025-11-30
Purpose: Strip HTML comment metadata blocks and internal TOCs from markdown files
Session-ID: 6f8970e0-023d-45dc-b3d8-5c9f9a8ff58e

Functions:
1. Remove HTML comment blocks (<!-- MERGE METADATA ... -->)
2. Remove internal table of contents (lists with anchor links)
3. Preserve actual content lists and headings
]]--

-- Track if we're in the first section of a file (where TOCs typically appear)
local in_first_section = true
local heading_count = 0

-- Function to check if a BulletList is an internal TOC
-- TOCs have characteristics:
-- - Appear near start of file (before first H2)
-- - Contain mostly links with anchor references (#heading-slug)
-- - Often have "Table of Contents" or "Contents" heading above
function is_internal_toc(bullet_list)
  if not in_first_section then
    return false
  end

  local total_items = 0
  local anchor_links = 0

  -- Walk through list items
  for i, item in pairs(bullet_list.content) do
    total_items = total_items + 1

    -- Check each item's content for links with anchors
    pandoc.walk_block(item, {
      Link = function(link)
        if link.target and string.match(link.target, "^#") then
          anchor_links = anchor_links + 1
        end
      end
    })
  end

  -- If >70% of items contain anchor links, likely a TOC
  if total_items > 0 and (anchor_links / total_items) > 0.7 then
    return true
  end

  return false
end

-- Main block filter
function Block(elem)
  -- Remove HTML comment blocks
  if elem.t == 'RawBlock' and elem.format == 'html' then
    if string.match(elem.text, '^%s*<!%-%-') then
      return {}  -- Remove by returning empty list
    end
  end

  -- Track heading count to know when we're past the intro/TOC section
  if elem.t == 'Header' and elem.level <= 2 then
    heading_count = heading_count + 1
    if heading_count > 1 then
      in_first_section = false
    end
  end

  -- Remove internal TOC bullet lists
  if elem.t == 'BulletList' then
    if is_internal_toc(elem) then
      return {}  -- Remove TOC
    end
  end

  return elem
end

-- Return the filter
return {
  {Block = Block}
}
