"""test_data.

Revision ID: 706a24bf5386
Revises: 54b52fbcb95c
Create Date: 2025-11-07 11:19:58.429459

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "706a24bf5386"
down_revision = "54b52fbcb95c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # === Activities ===
    conn.execute(
        sa.text(
            """
        INSERT INTO activities (id, name, parent_id) VALUES
        (1, 'Еда', NULL),
        (2, 'Мясная продукция', 1),
        (3, 'Молочная продукция', 1),
        (4, 'Автомобили', NULL),
        (5, 'Грузовые', 4),
        (6, 'Легковые', 4),
        (7, 'Запчасти', 6),
        (8, 'Аксессуары', 6),
        (9, 'Услуги', NULL),
        (10, 'Юридические', 9)
        """
        )
    )

    # === Buildings ===
    conn.execute(
        sa.text(
            """
        INSERT INTO buildings (id, address, latitude, longitude) VALUES
        (1, 'Москва, ул. Ленина, 1', 55.7558, 37.6176),
        (2, 'Санкт-Петербург, Невский пр., 10', 59.9311, 30.3609),
        (3, 'Екатеринбург, ул. Блюхера, 32/1', 56.8519, 60.6122),
        (4, 'Казань, ул. Баумана, 5', 55.7961, 49.1064),
        (5, 'Владивосток, ул. Светланская, 9', 43.1169, 131.8854)
        """
        )
    )

    # === Organizations ===
    conn.execute(
        sa.text(
            """
        INSERT INTO organizations (id, name, building_id) VALUES
        (1, 'ООО "Рога и Копыта"', 3),
        (2, 'ИП "Мясной Дом"', 1),
        (3, 'ООО "Молоко+"', 1),
        (4, 'ООО "ГрузТранс"', 2),
        (5, 'ООО "АвтоЛюкс"', 2),
        (6, 'ООО "Еда Маркет"', 4),
        (7, 'ООО "ЮрКонсалт"', 5),
        (8, 'ООО "БезТелефона"', 3),
        (9, 'ООО "БезДеятельности"', 4),
        (10, 'ООО "Рога и Копыта"', 1)
        """
        )
    )

    # === Organization-Activity mapping ===
    conn.execute(
        sa.text(
            """
        INSERT INTO organization_activity (organization_id, activity_id) VALUES
        (1, 2),
        (1, 3),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 6),
        (5, 8),
        (6, 1),
        (7, 10)
        """
        )
    )

    # === Phone Numbers ===
    conn.execute(
        sa.text(
            """
        INSERT INTO phone_numbers (id, phone_number, organization_id) VALUES
        (1, '+7 (222) 222-22-22', 1),
        (2, '+7 (923) 666-13-13', 1),
        (3, '+7 (495) 123-45-67', 2),
        (4, '+7 (812) 333-44-44', 5),
        (5, '+7 (423) 555-88-88', 7)
        """
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM phone_numbers"))
    conn.execute(sa.text("DELETE FROM organization_activity"))
    conn.execute(sa.text("DELETE FROM organizations"))
    conn.execute(sa.text("DELETE FROM buildings"))
    conn.execute(sa.text("DELETE FROM activities"))
