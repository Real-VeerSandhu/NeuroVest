class Alert < ApplicationRecord
  belongs_to :user
  has_many :notifications, dependent: :destroy

  validates :alert_type, presence: true, inclusion: { in: %w[price_threshold portfolio_performance simulation_outcome] }
  validates :condition_field, presence: true
  validates :condition_operator, presence: true, inclusion: { in: %w[> < >= <= == !=] }
  validates :condition_value, presence: true
  validates :is_active, inclusion: { in: [true, false] }

  scope :active, -> { where(is_active: true) }
  scope :by_type, ->(type) { where(alert_type: type) }

  def trigger!
    update!(triggered_at: Time.current)
    create_notification
  end

  private

  def create_notification
    notifications.create!(
      user: user,
      notification_type: alert_type,
      title: generate_title,
      message: generate_message,
      delivery_status: 'pending'
    )
  end

  def generate_title
    case alert_type
    when 'price_threshold'
      "Price Alert: #{condition_field}"
    when 'portfolio_performance'
      "Portfolio Performance Alert"
    when 'simulation_outcome'
      "Simulation Result Alert"
    end
  end

  def generate_message
    "Alert triggered: #{condition_field} #{condition_operator} #{condition_value}"
  end
end
