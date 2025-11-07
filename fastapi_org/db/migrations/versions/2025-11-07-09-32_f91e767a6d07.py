"""test data.

Revision ID: f91e767a6d07
Revises: c1e5c5efd868
Create Date: 2025-11-07 09:32:25.998724

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f91e767a6d07"
down_revision = "c1e5c5efd868"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
        INSERT INTO activities (id, name, parent_id) VALUES
        (1, 'IT и технологии', NULL),
        (2, 'Образование', NULL),
        (3, 'Медицина', NULL),
        (4, 'Общественное питание', NULL),
        (5, 'Логистика и транспорт', NULL),
        (6, 'Ритейл', NULL),
        (7, 'Разработка программного обеспечения', 1),
        (8, 'Техническая поддержка', 1),
        (9, 'Онлайн-обучение', 2),
        (10, 'Университеты и колледжи', 2),
        (11, 'Больницы и клиники', 3),
        (12, 'Аптеки', 3),
        (13, 'Кафе и рестораны', 4),
        (14, 'Фастфуд', 4),
        (15, 'Грузоперевозки', 5),
        (16, 'Такси и доставка', 5),
        (17, 'Супермаркеты', 6),
        (18, 'Интернет-магазины', 6),
        (19, 'Мобильная разработка', 7),
        (20, 'Веб-разработка', 7),
        (21, 'Корпоративное ПО', 7),
        (22, 'Техническая поддержка пользователей', 8),
        (23, 'DevOps и инфраструктура', 8),
        (24, 'Курсы программирования', 9),
        (25, 'Обучение дизайну', 9),
        (26, 'Медицинские центры', 11),
        (27, 'Частные клиники', 11),
        (28, 'Пиццерии', 13),
        (29, 'Кофейни', 13),
        (30, 'Электронная коммерция', 18)
        """
        )
    )

    conn.execute(
        sa.text(
            """
    INSERT INTO buildings (id, address, latitude, longitude) VALUES
    (1, 'Москва, ул. Ленина, 10', 55.7558, 37.6176),
    (2, 'Санкт-Петербург, Невский пр., 25', 59.9311, 30.3609),
    (3, 'Новосибирск, Красный пр., 12', 55.0084, 82.9357),
    (4, 'Екатеринбург, ул. Мира, 7', 56.8389, 60.6057),
    (5, 'Казань, ул. Баумана, 5', 55.7963, 49.1088),
    (6, 'Самара, ул. Ленинградская, 22', 53.1959, 50.1007),
    (7, 'Ростов-на-Дону, ул. Пушкина, 3', 47.2357, 39.7015),
    (8, 'Краснодар, ул. Северная, 18', 45.0355, 38.9753),
    (9, 'Нижний Новгород, ул. Горького, 8', 56.2965, 43.9361),
    (10, 'Воронеж, ул. Плехановская, 15', 51.6615, 39.2003)
    """
        )
    )

    conn.execute(
        sa.text(
            """
    INSERT INTO organizations (id, name, building_id) VALUES
    (1, 'SoftVision', 1),
    (2, 'TechForge', 1),
    (3, 'LearnOnline', 2),
    (4, 'MedStar Clinic', 3),
    (5, 'Health+ Pharmacy', 3),
    (6, 'PizzaPoint', 4),
    (7, 'CoffeeBeam', 4),
    (8, 'EduSpace University', 5),
    (9, 'CargoFlow Logistics', 6),
    (10, 'FastTrack Delivery', 6),
    (11, 'ShopGalaxy', 7),
    (12, 'FoodMart', 7),
    (13, 'CodeHub', 8),
    (14, 'DesignLab Academy', 8),
    (15, 'BurgerWorld', 9),
    (16, 'Cafe Verona', 10),
    (17, 'AutoDrive Taxi', 9),
    (18, 'eShop24', 10),
    (19, 'Clinic Nova', 5),
    (20, 'SmartSupport', 2)
    """
        )
    )

    conn.execute(
        sa.text(
            """
    INSERT INTO organization_activity (organization_id, activity_id) VALUES
    (1, 19),
    (2, 20),
    (3, 24),
    (4, 27),
    (5, 12),
    (6, 28),
    (7, 29),
    (8, 10),
    (9, 15),
    (10, 16),
    (11, 18),
    (12, 17),
    (13, 21),
    (14, 25),
    (15, 14),
    (16, 29),
    (17, 16),
    (18, 30),
    (19, 26),
    (20, 22)
    """
        )
    )

    conn.execute(
        sa.text(
            """
    INSERT INTO phone_numbers (id, phone_number, organization_id) VALUES
    (1, '+7 (900) 111-11-11', 1),
    (2, '+7 (900) 111-22-22', 2),
    (3, '+7 (900) 222-33-33', 3),
    (4, '+7 (900) 333-44-44', 4),
    (5, '+7 (900) 444-55-55', 5),
    (6, '+7 (900) 555-66-66', 6),
    (7, '+7 (900) 666-77-77', 7),
    (8, '+7 (900) 777-88-88', 8),
    (9, '+7 (900) 888-99-99', 9),
    (10, '+7 (900) 999-00-00', 10),
    (11, '+7 (901) 111-22-33', 11),
    (12, '+7 (901) 222-33-44', 12),
    (13, '+7 (901) 333-44-55', 13),
    (14, '+7 (901) 444-55-66', 14),
    (15, '+7 (901) 555-66-77', 15),
    (16, '+7 (901) 666-77-88', 16),
    (17, '+7 (901) 777-88-99', 17),
    (18, '+7 (901) 888-99-00', 18),
    (19, '+7 (902) 111-11-22', 19),
    (20, '+7 (902) 222-22-33', 20)
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
