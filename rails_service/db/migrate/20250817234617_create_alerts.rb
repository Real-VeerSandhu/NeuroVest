class CreateAlerts < ActiveRecord::Migration[8.0]
  def change
    create_table :alerts do |t|
      t.references :user, null: false, foreign_key: true
      t.string :alert_type
      t.string :condition_field
      t.string :condition_operator
      t.string :condition_value
      t.boolean :is_active
      t.datetime :triggered_at

      t.timestamps
    end
  end
end
