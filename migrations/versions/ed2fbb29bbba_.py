"""empty message

Revision ID: ed2fbb29bbba
Revises: 
Create Date: 2020-09-02 17:34:42.476315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2fbb29bbba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(length=264), nullable=True),
    sa.Column('max_capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('notion', sa.String(length=264), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('notion')
    )
    op.create_table('subnotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sub_notion', sa.String(length=264), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sub_notion')
    )
    op.create_table('exams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exam_title', sa.String(length=264), nullable=True),
    sa.Column('exam_type', sa.PickleType(), nullable=True),
    sa.Column('level', sa.PickleType(), nullable=True),
    sa.Column('time_for_completion', sa.Float(), nullable=True),
    sa.Column('notion_id', sa.Integer(), nullable=True),
    sa.Column('sub_notion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['notion_id'], ['notions.id'], ),
    sa.ForeignKeyConstraint(['sub_notion_id'], ['subnotions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_title', sa.String(length=264), nullable=True),
    sa.Column('question_text', sa.String(), nullable=True),
    sa.Column('qtype', sa.PickleType(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('wrong_answer1', sa.String(length=264), nullable=True),
    sa.Column('wrong_answer2', sa.String(length=264), nullable=True),
    sa.Column('wrong_answer3', sa.String(length=264), nullable=True),
    sa.Column('notion_id', sa.Integer(), nullable=True),
    sa.Column('sub_notion_id', sa.Integer(), nullable=True),
    sa.Column('is_exam', sa.Boolean(), nullable=True),
    sa.Column('is_test_exam', sa.Boolean(), nullable=True),
    sa.Column('level', sa.PickleType(), nullable=True),
    sa.Column('time_for_completion', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['notion_id'], ['notions.id'], ),
    sa.ForeignKeyConstraint(['sub_notion_id'], ['subnotions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=264), nullable=True),
    sa.Column('username', sa.String(length=264), nullable=True),
    sa.Column('email', sa.String(length=264), nullable=True),
    sa.Column('password', sa.String(length=264), nullable=True),
    sa.Column('role', sa.PickleType(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('exam_scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('exam', sa.Integer(), nullable=True),
    sa.Column('is_score_published', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['exam'], ['exams.id'], ),
    sa.ForeignKeyConstraint(['student'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exams_to_class',
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], )
    )
    op.create_table('exams_to_questions',
    sa.Column('quest_id', sa.Integer(), nullable=True),
    sa.Column('exam_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.ForeignKeyConstraint(['quest_id'], ['questions.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exams_to_questions')
    op.drop_table('exams_to_class')
    op.drop_table('exam_scores')
    op.drop_table('user')
    op.drop_table('questions')
    op.drop_table('exams')
    op.drop_table('subnotions')
    op.drop_table('notions')
    op.drop_table('class')
    # ### end Alembic commands ###
