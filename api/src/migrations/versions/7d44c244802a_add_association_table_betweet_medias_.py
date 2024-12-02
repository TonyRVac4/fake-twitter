"""add association table betweet Medias and Tweets

Revision ID: 7d44c244802a
Revises: 7928e66a7ad7
Create Date: 2024-11-28 14:29:26.550766

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d44c244802a"
down_revision: Union[str, None] = "7928e66a7ad7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "medias_tweets",
        sa.Column("tweet_id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["media_id"],
            ["medias.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["tweet_id"],
            ["tweets.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("tweet_id", "media_id"),
        sa.UniqueConstraint("tweet_id", "media_id", name="unique_media_tweet"),
    )
    op.drop_constraint("medias_tweet_id_fkey", "medias", type_="foreignkey")
    op.drop_column("medias", "tweet_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "medias",
        sa.Column(
            "tweet_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "medias_tweet_id_fkey",
        "medias",
        "tweets",
        ["tweet_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_table("medias_tweets")
    # ### end Alembic commands ###
