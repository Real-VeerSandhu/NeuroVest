class CreateUsers < ActiveRecord::Migration[8.0]
  def change
    create_table :users do |t|
      t.string :external_user_id
      t.string :email
      t.text :notification_preferences

      t.timestamps
    end
  end
end
