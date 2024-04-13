---@meta
-- Generated by PZEventDoc https://github.com/demiurgeQuantified/PZEventDoc

-- If it helped you, please consider leaving me a tip ^u^
-- https://ko-fi.com/starseamstress

---@class ContextMenuItemStack Data about a selected item stack.
---@field items table<integer, InventoryItem> List of items in the stack. The first item is repeated as the second element.
---@field count integer The number of items in the stack (including the doubled up first item).
---@field equipped boolean Whether the item is equipped.
---@field inHotbar boolean? Whether the item is taking up a slot on the player's hotbar. Sometimes nil.
---@field invPanel ISInventoryPane The inventory panel the item belongs to.
---@field name string Translated name of the item. <br> 'equipped:' is prepended if it is equipped. <br> 'hotbar:' is prepended if the item is in the hotbar, but not equipped.
---@field cat string Untranslated item category.
---@field weight number Weight of the stack.

---@class MngInvItemData Data about a specific item stack in a player's inventory.
---@field fullType string Full type of the item.
---@field itemId integer ID of the item.
---@field isEquip boolean Whether the item is equipped.
---@field var number The used delta if the item is a drainable, or the item's condition if not.
---@field count string The amount of items.
---@field cat string The category of the item.
---@field parrentId integer Item ID of the container this item is inside. -1 if it is not in a container
---@field hasParrent boolean Whether the item has a parent.
---@field container string Type of the container.
---@field inInv boolean Always false?

---@class MngInvItemTable Table containing details of another player's inventory.
---@field capacityWeight number Total weight of items in the inventory.
---@field maxWeight number Maximum weight the inventory can contain.
---@field [integer] MngInvItemData Item stack data entries.

-- TODO: idk what this really is lol
---@class DBSchemaEntry
---@field name string
---@field type string

---@alias PlayerDamageType
---| '"POISON"' # Damage from poison.
---| '"HUNGRY"' # Damage from hunger.
---| '"SICK"' # Damage from sickness.
---| '"BLEEDING"' # Damage from bleeding wounds.
---| '"THIRST"' # Damage from thirst.
---| '"HEAVYLOAD"' # Damage from over encumbrance.
---| '"INFECTION"' # Damage from zombie infection.
---| '"LOWWEIGHT"' # Damage from being severely underweight.
---| '"FALLDOWN"' # Damage from falling.
---| '"WEAPONHIT"' # Damage from being hit by weapons.
---| '"CARHITDAMAGE"' # Damage from being hit by a car.
---| '"CARCRASHDAMAGE"' # Damage from being inside a car when it crashes.
