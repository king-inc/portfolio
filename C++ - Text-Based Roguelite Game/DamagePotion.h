#pragma once

#include "Item.h"

class DamagePotion : public Item
{
public:
	DamagePotion(int damage)
	void use(temp::GameObject* hit) override;
	
	IMPLEMENT_ITEM_NAME("Damage Potion")
	IMPLEMENT_ITEM_ID(ItemID::DAMAGE_POTION)


private:
	int m_dmg;
}
