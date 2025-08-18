class PortfolioSummary < ApplicationRecord
  belongs_to :user

  validates :summary_type, presence: true, inclusion: { in: %w[daily weekly monthly] }
  validates :period_start, presence: true
  validates :period_end, presence: true
  validates :total_value, presence: true, numericality: { greater_than_or_equal_to: 0 }
  validates :performance_percentage, presence: true, numericality: true

  scope :by_type, ->(type) { where(summary_type: type) }
  scope :recent, -> { order(generated_at: :desc) }

  def self.generate_summary(user, type, start_date, end_date)
    # This would integrate with your portfolio service
    # For now, we'll create a mock summary
    create!(
      user: user,
      summary_type: type,
      period_start: start_date,
      period_end: end_date,
      total_value: rand(10000..100000),
      performance_percentage: rand(-10.0..15.0).round(2),
      generated_at: Time.current
    )
  end
end
