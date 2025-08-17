class Notification < ApplicationRecord
  belongs_to :user
  belongs_to :alert, optional: true

  validates :notification_type, presence: true, inclusion: { in: %w[price_threshold portfolio_performance simulation_outcome daily_summary weekly_summary] }
  validates :title, presence: true
  validates :message, presence: true
  validates :delivery_status, presence: true, inclusion: { in: %w[pending delivered failed] }

  scope :pending, -> { where(delivery_status: 'pending') }
  scope :delivered, -> { where(delivery_status: 'delivered') }
  scope :by_type, ->(type) { where(notification_type: type) }

  def mark_as_delivered!
    update!(delivery_status: 'delivered', delivered_at: Time.current)
  end

  def mark_as_failed!
    update!(delivery_status: 'failed')
  end
end
