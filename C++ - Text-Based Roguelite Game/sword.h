#pragma once

#include "Item.h"

class sword : public Item
{
public:
	sword(int damage)
	void use(temp::Object* hit) override;
	
	IMPLEMENT_ITEM_NAME("sword")
	IMPLEMENT_ITEM_ID(ItemID::SWORD)


private:
	int m_dmg;
}
