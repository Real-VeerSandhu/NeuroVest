class User < ApplicationRecord
  has_many :alerts, dependent: :destroy
  has_many :notifications, dependent: :destroy
  has_many :portfolio_summaries, dependent: :destroy

  validates :external_user_id, presence: true, uniqueness: true
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }

  serialize :notification_preferences, JSON

  def notification_preferences
    super || {
      email_enabled: true,
      price_alerts: true,
      portfolio_updates: true,
      daily_summaries: false,
      weekly_summaries: true
    }
  end
end
