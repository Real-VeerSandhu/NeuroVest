# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.0].define(version: 2025_08_17_234708) do
  create_table "alerts", force: :cascade do |t|
    t.integer "user_id", null: false
    t.string "alert_type"
    t.string "condition_field"
    t.string "condition_operator"
    t.string "condition_value"
    t.boolean "is_active"
    t.datetime "triggered_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id"], name: "index_alerts_on_user_id"
  end

  create_table "notifications", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "alert_id", null: false
    t.string "notification_type"
    t.string "title"
    t.text "message"
    t.datetime "delivered_at"
    t.string "delivery_status"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["alert_id"], name: "index_notifications_on_alert_id"
    t.index ["user_id"], name: "index_notifications_on_user_id"
  end

  create_table "portfolio_summaries", force: :cascade do |t|
    t.integer "user_id", null: false
    t.string "summary_type"
    t.date "period_start"
    t.date "period_end"
    t.decimal "total_value"
    t.decimal "performance_percentage"
    t.datetime "generated_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["user_id"], name: "index_portfolio_summaries_on_user_id"
  end

  create_table "users", force: :cascade do |t|
    t.string "external_user_id"
    t.string "email"
    t.text "notification_preferences"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_foreign_key "alerts", "users"
  add_foreign_key "notifications", "alerts"
  add_foreign_key "notifications", "users"
  add_foreign_key "portfolio_summaries", "users"
end
