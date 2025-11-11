"""indexes.

Revision ID: 6234f69c327a
Revises: 706a24bf5386
Create Date: 2025-11-11 11:45:29.479356

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6234f69c327a"
down_revision = "706a24bf5386"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "idx_buildings_latitude_longitude",
        "buildings",
        ["latitude", "longitude"],
    )
    op.create_index("idx_buildings_latitude", "buildings", ["latitude"])
    op.create_index("idx_buildings_longitude", "buildings", ["longitude"])

    op.create_index("idx_buildings_address", "buildings", ["address"])

    op.create_index("idx_organizations_building_id", "organizations", ["building_id"])
    op.create_index("idx_organizations_name", "organizations", ["name"])
    op.create_index(
        "idx_organizations_name_lower",
        "organizations",
        [sa.text("lower(name)")],
    )

    op.create_index("idx_activities_parent_id", "activities", ["parent_id"])
    op.create_index("idx_activities_name", "activities", ["name"])

    op.create_index(
        "idx_org_activity_org_id_activity_id",
        "organization_activity",
        ["organization_id", "activity_id"],
    )
    op.create_index(
        "idx_org_activity_activity_id_org_id",
        "organization_activity",
        ["activity_id", "organization_id"],
    )

    op.create_index(
        "idx_phone_numbers_organization_id",
        "phone_numbers",
        ["organization_id"],
    )
    op.create_index("idx_phone_numbers_phone", "phone_numbers", ["phone_number"])


def downgrade() -> None:
    op.drop_index("idx_buildings_latitude_longitude", table_name="buildings")
    op.drop_index("idx_buildings_latitude", table_name="buildings")
    op.drop_index("idx_buildings_longitude", table_name="buildings")
    op.drop_index("idx_buildings_address", table_name="buildings")

    op.drop_index("idx_organizations_building_id", table_name="organizations")
    op.drop_index("idx_organizations_name", table_name="organizations")
    op.drop_index("idx_organizations_name_lower", table_name="organizations")

    op.drop_index("idx_activities_parent_id", table_name="activities")
    op.drop_index("idx_activities_name", table_name="activities")

    op.drop_index(
        "idx_org_activity_org_id_activity_id",
        table_name="organization_activity",
    )
    op.drop_index(
        "idx_org_activity_activity_id_org_id",
        table_name="organization_activity",
    )

    op.drop_index("idx_phone_numbers_organization_id", table_name="phone_numbers")
    op.drop_index("idx_phone_numbers_phone", table_name="phone_numbers")
