class CreatePortfolioSummaries < ActiveRecord::Migration[8.0]
  def change
    create_table :portfolio_summaries do |t|
      t.references :user, null: false, foreign_key: true
      t.string :summary_type
      t.date :period_start
      t.date :period_end
      t.decimal :total_value
      t.decimal :performance_percentage
      t.datetime :generated_at

      t.timestamps
    end
  end
end
